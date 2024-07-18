const express = require('express');
const multer = require('multer');
const path = require('path');
const ffmpeg = require('ffmpeg-static');
const { spawn } = require('child_process');
const fs = require('fs');
const Queue = require('bull');
const NodeCache = require('node-cache');
const schedule = require('node-schedule');

const app = express();
const port = process.env.PORT || 3000;

// Create a new queue
const videoQueue = new Queue('video processing');

// Create a new cache
const videoCache = new NodeCache({ stdTTL: 3600, checkperiod: 600 });

// Multer configuration for file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, path.join(__dirname, '..', 'temp')) // Store uploaded files in the 'temp' directory
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + path.extname(file.originalname)) // Use timestamp as filename to avoid conflicts
  }
});

// Configure multer with storage options and file size limit
const upload = multer({ 
  storage: storage,
  limits: { fileSize: 1024 * 1024 * 1024 }, // 1GB file size limit
  fileFilter: (req, file, cb) => {
    if (file.mimetype !== 'video/mp4') {
      return cb(new Error('Only MP4 files are allowed'), false);
    }
    cb(null, true);
  }
});

// Serve static files from the frontend directory
app.use(express.static(path.join(__dirname, '..', 'frontend')));

// File upload route
app.post('/upload', (req, res) => {
  upload.single('video')(req, res, (err) => {
    if (err instanceof multer.MulterError) {
      if (err.code === 'LIMIT_FILE_SIZE') {
        return res.status(400).json({ error: 'File size exceeds the 1GB limit.' });
      }
      return res.status(400).json({ error: 'Error uploading file.' });
    } else if (err) {
      return res.status(400).json({ error: err.message });
    }
    
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded.' });
    }
    res.json({ filename: req.file.filename });
  });
});

// Video processing route
app.post('/trim', express.json(), (req, res) => {
  const { filename, startTime, endTime } = req.body;
  
  if (!filename || !startTime || !endTime) {
    return res.status(400).json({ error: 'Missing required parameters.' });
  }
  
  if (isNaN(startTime) || isNaN(endTime) || startTime < 0 || endTime <= startTime) {
    return res.status(400).json({ error: 'Invalid start or end time.' });
  }

  const jobId = Date.now().toString();

  // Check if the trimmed video is already in cache
  const cacheKey = `${filename}_${startTime}_${endTime}`;
  const cachedVideo = videoCache.get(cacheKey);

  if (cachedVideo) {
    console.log('Returning cached video');
    return res.json({ jobId, cached: true });
  }

  // Add job to the queue
  videoQueue.add({
    jobId,
    filename,
    startTime,
    endTime,
    cacheKey
  });

  res.json({ jobId, cached: false });
});

// Job progress route
app.get('/progress/:jobId', (req, res) => {
  const { jobId } = req.params;
  videoQueue.getJob(jobId).then((job) => {
    if (job === null) {
      res.status(404).json({ error: 'Job not found' });
    } else {
      job.getState().then((state) => {
        res.json({ jobId, state, progress: job.progress() });
      });
    }
  }).catch(err => {
    res.status(500).json({ error: 'Error fetching job progress' });
  });
});

// Process jobs in the queue
videoQueue.process(async (job) => {
  const { jobId, filename, startTime, endTime, cacheKey } = job.data;
  const inputPath = path.join(__dirname, '..', 'temp', filename);
  const outputPath = path.join(__dirname, '..', 'temp', `trimmed_${filename}`);

  // Check if input file exists
  if (!fs.existsSync(inputPath)) {
    throw new Error('Input file not found');
  }

  console.log(`Starting video trim: ${filename} from ${startTime} to ${endTime}`);

  return new Promise((resolve, reject) => {
    const ffmpegProcess = spawn(ffmpeg, [
      '-i', inputPath,
      '-ss', startTime,
      '-to', endTime,
      '-c', 'copy',
      outputPath
    ]);

    ffmpegProcess.stderr.on('data', (data) => {
      console.log(`FFmpeg stderr: ${data}`);
      // Update job progress (this is a simple example, you might want to parse the FFmpeg output for more accurate progress)
      job.progress(50);
    });

    ffmpegProcess.on('close', (code) => {
      if (code === 0) {
        console.log('Video trimming completed successfully');
        job.progress(100);
        // Cache the trimmed video
        videoCache.set(cacheKey, outputPath);
        resolve(outputPath);
      } else {
        console.error(`FFmpeg process exited with code ${code}`);
        reject(new Error('Error processing video'));
      }
    });
  });
});

// Download route
app.get('/download/:jobId', (req, res) => {
  const { jobId } = req.params;
  videoQueue.getJob(jobId).then((job) => {
    if (job === null) {
      res.status(404).json({ error: 'Job not found' });
    } else {
      const { cacheKey } = job.data;
      const cachedPath = videoCache.get(cacheKey);
      const outputPath = cachedPath || path.join(__dirname, '..', 'temp', `trimmed_${job.data.filename}`);

      if (!fs.existsSync(outputPath)) {
        return res.status(404).json({ error: 'Trimmed video file not found' });
      }

      res.download(outputPath, (err) => {
        if (err) {
          console.error('Error sending file:', err);
          res.status(500).json({ error: 'Error sending file' });
        }
        // Don't delete cached files
        if (!cachedPath) {
          // Clean up temporary files
          fs.unlink(path.join(__dirname, '..', 'temp', job.data.filename), (err) => {
            if (err) console.error('Error deleting input file:', err);
          });
          fs.unlink(outputPath, (err) => {
            if (err) console.error('Error deleting output file:', err);
          });
        }
      });
    }
  }).catch(err => {
    res.status(500).json({ error: 'Error processing download request' });
  });
});

// Function to clean up old files
const cleanupOldFiles = () => {
  const tempDir = path.join(__dirname, '..', 'temp');
  const now = Date.now();
  const maxAge = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

  fs.readdir(tempDir, (err, files) => {
    if (err) {
      console.error('Error reading temp directory:', err);
      return;
    }

    files.forEach(file => {
      const filePath = path.join(tempDir, file);
      fs.stat(filePath, (err, stats) => {
        if (err) {
          console.error(`Error getting file stats for ${file}:`, err);
          return;
        }

        if (now - stats.mtime.getTime() > maxAge) {
          fs.unlink(filePath, err => {
            if (err) {
              console.error(`Error deleting old file ${file}:`, err);
            } else {
              console.log(`Deleted old file: ${file}`);
            }
          });
        }
      });
    });
  });
};

// Schedule cleanup job to run every day at midnight
schedule.scheduleJob('0 0 * * *', cleanupOldFiles);

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
