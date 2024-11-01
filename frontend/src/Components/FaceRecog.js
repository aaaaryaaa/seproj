import React from 'react';

const FaceRecog = () => {
  return (
    <div>
      <h1>Live Face Detection</h1>
      <img
        src="http://127.0.0.1:5000/video_feed" // Ensure this URL matches your Flask server's IP/port
        alt="Live Video Feed"
        style={{ width: '100%', height: 'auto' }}
      />
    </div>
  );
};

export default FaceRecog;
