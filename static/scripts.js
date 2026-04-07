// // scripts.js

// function navigateTo(page) {
//     if (page === 'webcam') {
//         window.location.href = '/webcam';
//     } else if (page === 'upload_photo') {
//         window.location.href = '/upload_photo';
//     } else if (page === 'upload_video') {
//         window.location.href = '/upload_video';
//     }
// }

// // Start webcam streaming
// function startWebcam() {
//     // Set the webcam image source to the webcam feed endpoint
//     const webcamFeed = document.querySelector('img[alt="Webcam Feed"]');
//     webcamFeed.src = "/webcam"; // Endpoint should stream frames
// }

// // Upload an image file
// function uploadFile() {
//     const fileInput = document.getElementById('upload');
//     const formData = new FormData();
//     formData.append('file', fileInput.files[0]);

//     fetch('/upload', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         // Display the result image
//         const resultImage = document.createElement('img');
//         resultImage.src = `/output/${data.result_image}`;
//         document.getElementById('results').appendChild(resultImage);
//     })
//     .catch(error => console.error('Error uploading file:', error));
// }

// // Upload a video file
// function uploadVideoFile() {
//     const videoInput = document.getElementById('uploadVideo');
//     const formData = new FormData();
//     formData.append('file', videoInput.files[0]);

//     fetch('/upload_video', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         document.getElementById('results').innerHTML = '<p>Video processed</p>';
//     })
//     .catch(error => console.error('Error uploading video:', error));
// }

// function navigateTo(page) {
//     if (page === 'webcam') {
//         window.location.href = '/webcam';
//     } else if (page === 'upload_photo') {
//         window.location.href = '/upload_photo';
//     } else if (page === 'upload_video') {
//         window.location.href = '/upload_video';
//     }
// }

// function uploadFile(event) {
//     event.preventDefault();
//     const fileInput = document.getElementById('upload');
//     const formData = new FormData();
//     formData.append('file', fileInput.files[0]);

//     fetch('/upload', {
//         method: 'POST',
//         body: formData
//     })
//     .then(response => response.json())
//     .then(data => {
//         const resultImage = document.createElement('img');
//         resultImage.src = /output/${data.result_image};
//         document.getElementById('results').appendChild(resultImage);
//     })
//     .catch(error => console.error('Error uploading file:', error));
// }