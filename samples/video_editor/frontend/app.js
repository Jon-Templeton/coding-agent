document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const video = document.getElementById('video');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const seekBar = document.getElementById('seek-bar');
    const currentTime = document.getElementById('current-time');
    const duration = document.getElementById('duration');
    const startTimeInput = document.getElementById('start-time-input');
    const endTimeInput = document.getElementById('end-time-input');
    const trimBtn = document.getElementById('trim-btn');
    const progressBar = document.getElementById('progress-bar');
    const timeline = document.getElementById('timeline');
    const trimStart = document.getElementById('trim-start');
    const trimEnd = document.getElementById('trim-end');
    const trimSelection = document.getElementById('trim-selection');
    const trimProgress = document.getElementById('trim-progress');
    const errorMessage = document.getElementById('error-message');
    const dropArea = document.getElementById('drop-area');

    let isDragging = false;
    let currentHandle = null;
    let uploadedFileName = '';
    let currentJobId = null;

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 5000);
    }

    // Drag and drop functionality
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropArea.classList.add('highlight');
    }

    function unhighlight() {
        dropArea.classList.remove('highlight');
    }

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const file = dt.files[0];
        handleFile(file);
    }

    dropArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        handleFile(e.target.files[0]);
    });

    function handleFile(file) {
        if (file.size > 1024 * 1024 * 1024) {
            showError('File size exceeds the 1GB limit.');
            return;
        }

        if (file.type !== 'video/mp4') {
            showError('Only MP4 files are allowed.');
            return;
        }

        fileInput.files = new FileList([file]);
        uploadBtn.click();
    }

    uploadBtn.addEventListener('click', () => {
        if (fileInput.files.length === 0) {
            showError('Please select a file first.');
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('video', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(result => {
            console.log(result);
            uploadedFileName = result.filename;
            initializeLazyLoading(file);
        })
        .catch(error => {
            console.error('Error:', error);
            showError(error.error || 'An error occurred during upload.');
        });
    });

    function initializeLazyLoading(file) {
        const fileURL = URL.createObjectURL(file);
        video.src = fileURL;
        video.preload = 'metadata';

        video.addEventListener('loadedmetadata', () => {
            seekBar.max = video.duration;
            duration.textContent = formatTime(video.duration);
            resetTrimHandles();
            video.preload = 'auto';
        });

        video.addEventListener('canplay', () => {
            playPauseBtn.disabled = false;
        });

        // Load only the first few seconds initially
        video.addEventListener('loadeddata', () => {
            video.currentTime = 0;
        });
    }

    playPauseBtn.addEventListener('click', togglePlayPause);

    video.addEventListener('timeupdate', updateVideoProgress);

    seekBar.addEventListener('input', () => {
        video.currentTime = seekBar.value;
    });

    trimStart.addEventListener('mousedown', (e) => startDragging(e, trimStart));
    trimEnd.addEventListener('mousedown', (e) => startDragging(e, trimEnd));

    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', stopDragging);

    trimBtn.addEventListener('click', () => {
        if (!uploadedFileName) {
            showError('Please upload a video first.');
            return;
        }

        const start = parseFloat(trimStart.style.left) / 100 * video.duration;
        const end = parseFloat(trimEnd.style.left) / 100 * video.duration;

        fetch('/trim', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ filename: uploadedFileName, startTime: start, endTime: end }),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(data => {
            currentJobId = data.jobId;
            trimProgress.style.display = 'block';
            checkJobProgress();
        })
        .catch(error => {
            console.error('Error:', error);
            showError(error.error || 'An error occurred during trimming.');
        });
    });

    function checkJobProgress() {
        fetch(`/progress/${currentJobId}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.json();
        })
        .then(data => {
            trimProgress.textContent = `Trim progress: ${data.progress}%`;
            if (data.state === 'completed') {
                downloadTrimmedVideo();
            } else if (data.state === 'failed') {
                throw new Error('Job failed');
            } else {
                setTimeout(checkJobProgress, 1000);
            }
        })
        .catch(error => {
            console.error('Error checking job progress:', error);
            showError('Error checking trim progress. Please try again.');
            trimProgress.style.display = 'none';
        });
    }

    function downloadTrimmedVideo() {
        fetch(`/download/${currentJobId}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err; });
            }
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'trimmed_video.mp4';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            trimProgress.style.display = 'none';
        })
        .catch(error => {
            console.error('Error downloading trimmed video:', error);
            showError(error.error || 'An error occurred while downloading the trimmed video.');
            trimProgress.style.display = 'none';
        });
    }

    function formatTime(seconds) {
        const minutes = Math.floor(seconds / 60);
        seconds = Math.floor(seconds % 60);
        return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }

    function togglePlayPause() {
        if (video.paused) {
            video.play();
            playPauseBtn.textContent = 'Pause';
        } else {
            video.pause();
            playPauseBtn.textContent = 'Play';
        }
    }

    function updateVideoProgress() {
        seekBar.value = video.currentTime;
        currentTime.textContent = formatTime(video.currentTime);
        progressBar.style.width = `${(video.currentTime / video.duration) * 100}%`;
    }

    function resetTrimHandles() {
        trimStart.style.left = '0%';
        trimEnd.style.left = '100%';
        updateTrimSelection();
        updateTrimInputs();
    }

    function startDragging(e, handle) {
        isDragging = true;
        currentHandle = handle;
    }

    function drag(e) {
        if (!isDragging) return;

        const timelineRect = timeline.getBoundingClientRect();
        let position = (e.clientX - timelineRect.left) / timelineRect.width;
        position = Math.max(0, Math.min(position, 1));

        if (currentHandle === trimStart) {
            const endPosition = parseFloat(trimEnd.style.left) / 100;
            if (position < endPosition) {
                currentHandle.style.left = `${position * 100}%`;
            }
        } else if (currentHandle === trimEnd) {
            const startPosition = parseFloat(trimStart.style.left) / 100;
            if (position > startPosition) {
                currentHandle.style.left = `${position * 100}%`;
            }
        }

        updateTrimSelection();
        updateTrimInputs();
    }

    function stopDragging() {
        isDragging = false;
        currentHandle = null;
    }

    function updateTrimSelection() {
        const startPosition = parseFloat(trimStart.style.left);
        const endPosition = parseFloat(trimEnd.style.left);
        trimSelection.style.left = `${startPosition}%`;
        trimSelection.style.width = `${endPosition - startPosition}%`;
    }

    function updateTrimInputs() {
        const startTime = (parseFloat(trimStart.style.left) / 100) * video.duration;
        const endTime = (parseFloat(trimEnd.style.left) / 100) * video.duration;
        startTimeInput.value = formatTime(startTime);
        endTimeInput.value = formatTime(endTime);
    }

    // Enhanced keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space') {
            e.preventDefault();
            togglePlayPause();
        } else if (e.code === 'ArrowLeft') {
            e.preventDefault();
            video.currentTime -= 5;
        } else if (e.code === 'ArrowRight') {
            e.preventDefault();
            video.currentTime += 5;
        } else if (e.code === 'KeyI') {
            e.preventDefault();
            const currentPosition = (video.currentTime / video.duration) * 100;
            trimStart.style.left = `${currentPosition}%`;
            updateTrimSelection();
            updateTrimInputs();
        } else if (e.code === 'KeyO') {
            e.preventDefault();
            const currentPosition = (video.currentTime / video.duration) * 100;
            trimEnd.style.left = `${currentPosition}%`;
            updateTrimSelection();
            updateTrimInputs();
        }
    });
});
