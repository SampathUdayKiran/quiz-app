

// navigator.mediaDevices
// .getUserMedia({ video: true })
// .then(function (stream) {
//     const videoElement = document.getElementById('camera');
//     videoElement.srcObject = stream;
// })
// .catch(function (error) {
//     console.error('Error accessing the camera: ', error);
// });

// window.onbeforeunload = function() {
//     console.log('HII')
//     return "Are you sure you want to reload this page?";
// };

// const videoElement = document.getElementById("camera");
// const startRecordButton = document.getElementById("startRecord");
// const stopRecordButton = document.getElementById("stopRecord");
// const recordedVideo = document.getElementById("recorded");
// let mediaRecorder;
// let recordedChunks = [];

// // Access the user's camera and display the camera feed
// navigator.mediaDevices
//   .getUserMedia({ video: true })
//   .then(function (stream) {
//     videoElement.srcObject = stream;
//     mediaRecorder = new MediaRecorder(stream);

//     // mediaRecorder.ondataavailable = (event) => {
//     //   if (event.data.size > 0) {
//     //     recordedChunks.push(event.data);
//     //     console.log(recordedChunks);
//     //   }
//     // };

//     // mediaRecorder.onstop = () => {
//     //   const blob = new Blob(recordedChunks, { type: "video/webm" });
//     //   const url = URL.createObjectURL(blob);
//     //   recordedVideo.src = url;
//     // };
//   })
//   .catch(function (error) {
//     console.error("Error accessing the camera: ", error);
//   });

// Start video recording
// startRecordButton.addEventListener("click", () => {
//   mediaRecorder.start();
//   startRecordButton.disabled = true;
//   stopRecordButton.disabled = false;
// });

// // Stop video recording
// stopRecordButton.addEventListener("click", () => {
//   mediaRecorder.stop();
//   startRecordButton.disabled = false;
//   stopRecordButton.disabled = true;
// });
