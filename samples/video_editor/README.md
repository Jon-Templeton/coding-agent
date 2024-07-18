# Web-based Video Editor

A lightweight, browser-based video editing tool that allows users to upload, play, and trim MP4 videos up to 1GB in size.

## Features

- Drag-and-drop or click-to-upload functionality for MP4 files
- Custom video player with play/pause and seeking controls
- Visual timeline for precise video trimming
- Server-side video processing using FFmpeg
- Responsive design for desktop use
- Keyboard shortcuts for enhanced usability
- Progress tracking for trim operations
- Automatic cleanup of temporary files

## Tech Stack

- Frontend: HTML, CSS, JavaScript
- Backend: Node.js with Express.js
- Video Processing: FFmpeg
- File Upload: Multer middleware
- Queue Management: Bull
- Caching: Node-cache

## Prerequisites

- Node.js (v14 or later recommended)
- FFmpeg installed on the server

## Installation

1. Clone the repository:
`git clone https://github.com/yourusername/web-based-video-editor.git`
`cd web-based-video-editor`
2. Install dependencies: `npm install`
3. Create a `temp` directory in the project root for temporary file storage
4. Set up environment variables:
Create a `.env` file in the project root and add the following:
`PORT=3000`
## Usage

1. Start the server: `npm start`
2. Open a web browser and navigate to `http://localhost:3000`

3. Upload an MP4 video file (up to 1GB) using drag-and-drop or the file input

4. Use the video player controls to preview your video

5. Set the start and end points for trimming using the timeline handles or time input fields

6. Click "Trim Video" to process your selection

7. Once processing is complete, the trimmed video will be available for download

## Keyboard Shortcuts

- Space: Play/Pause video
- Left Arrow: Seek backward 5 seconds
- Right Arrow: Seek forward 5 seconds
- I: Set trim start point to current time
- O: Set trim end point to current time

## Development

To run the project in development mode with auto-reloading: `npm run dev`

## Cleanup

The server automatically cleans up temporary files older than 24 hours. This job runs daily at midnight.

## Known Limitations

- Only supports MP4 video format
- Maximum file size is 1GB
- Designed for desktop use; mobile support is limited