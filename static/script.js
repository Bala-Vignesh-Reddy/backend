// const socket = io();
// const feedImage = document.getElementById('feed-image')  
// const feedImage0 = document.getElementById('feed-image-0');
// const feedImage1 = document.getElementById('feed-image-1');
// const artifactList = document.getElementById('artifact-list').querySelector('ul');
// const artifactDetails = document.getElementById('artifact-info');
// const notificationList = document.getElementById('notification-list');
// const maintenanceInfo = document.getElementById('maintenance-info');

// const checkAlignmentButton = document.getElementById('check-alignment-button');
// const alignmentResult = document.getElementById('alignment-result');


function fetchArtifacts() {
  console.log("Fetching artifacts..")
  fetch('/artifacts')
    .then(response => response.json())
    .then(artifacts => {
      const exhibitTable = document.querySelector('.table-section table');
      const tbody = exhibitTable.querySelector('tbody'); // Get the table body
      tbody.innerHTML = ''; // Clear existing rows

      const headerRow = document.createElement('tr');
      headerRow.innerHTML = `
        <th>Id</th>
        <th>Name</th>
        <th>Status</th>
      `;
      tbody.appendChild(headerRow);

      artifacts.forEach(artifact => {
        const row = document.createElement('tr');
        const idCell = document.createElement('td');
        const nameCell = document.createElement('td');
        const statusCell = document.createElement('td');

        idCell.textContent = artifact.id;
        nameCell.textContent = artifact.name;
        statusCell.textContent = artifact.status;

        row.appendChild(idCell);
        row.appendChild(nameCell);
        row.appendChild(statusCell);
        tbody.appendChild(row);
      });
    })
    .catch(error => console.error('Error fetching artifacts:', error));
}

const notificationSection = document.querySelector('.notification-section');

function checkForProximityAlerts() {
  console.log("Fetching proximity alerts...");
  fetch('/api/proximity_alerts')
    .then(response => response.json())
    .then(alerts => {
      alerts.forEach(alert => {
        const existingNotification = document.querySelector(`.notification-section p:contains("${alert.message}")`);
        if(existingNotification){
          return;
        }
        const notification = document.createElement('p');
        notification.innerHTML = `
          <strong>Proximity Alert!</strong><br>
          Location: ${alert.location}<br>
          Timestamp: ${alert.timestamp}
          <button class="close-notification">Close</button> </div>
        `;
        notificationSection.appendChild(notification);

        const closeButton = notification.querySelector('.close-notification');
        closeButton.addEventListener('click', () => {
          notificationSection.removeChild(notification);
        })
      });
    })
    .catch(error => console.error('Error fetching proximity alerts:', error));
}
// setInterval(checkForProximityAlerts, 5000);

function updateDateTime() {
  const now = new Date();
  const dateTimeString = now.toLocaleString();
  document.getElementById('date-time').textContent = dateTimeString;
}

setInterval(updateDateTime, 1000);

document.addEventListener('DOMContentLoaded', () => {
  fetchArtifacts();
 })


const warningBar = document.getElementById('warning-bar');
setTimeout(() => {
  warningBar.textContent = "Warning: Anomaly detected!";
  warningBar.style.backgroundColor = "red"; 
}, 5000);
// var videoElement = document.getElementById('video')
//   function reloadVideoFeed(){
//     videoElement.src = "{{ url_for('video_feed') }}" + "?rand=" + new Date().getTime()
//   }
//   reloadVideoFeed()

// function checkForWarnings() {
//   fetch('/api/warnings')
//     .then(response => response.json())
//     .then(warnings => {
//       const warningBar = document.getElementById('warning-bar');
//       if (warnings.length > 0) {
//         const warning = warnings[0]; // Display the first warning
//         warningBar.textContent = `Warning: ${warning.message} - Location: ${warning.location} - Time: ${warning.timestamp}`;
//         warningBar.style.backgroundColor = "red";
//       } else {
//         warningBar.textContent = "";
//         warningBar.style.backgroundColor = "transparent";
//       }
//     })
//     .catch(error => console.error('Error fetching warnings:', error));
// }

// // Check for warnings every 5 seconds
// setInterval(checkForWarnings, 5000);

// function fetchArtifactDetails(id) {
//     fetch(`/artifacts/${id}`)
//         .then(response => response.json())
//         .then(artifact => {
//             artifactDetails.innerHTML = ''; // Clear previous details
//             const details = `
//                 <h3>${artifact.name}</h3>
//                 <p>${artifact.description}</p>
//                 <p>Status: ${artifact.status}</p>
//                 <img src="${artifact.image_path}" alt="${artifact.name}">
//             `;
//             artifactDetails.innerHTML = details;
//         });
// }

// // function fetchDetectionNotifications() {
// //   fetch('/detections')
// //     .then(response => response.json())
// //     .then(notifications => {
// //       notificationList.innerHTML = '';
// //       notifications.forEach(notification => {
// //         const li = document.createElement('li');
// //         li.innerHTML = `
// //           <strong>Artifact ID: ${notification.artifact_id}</strong><br>
// //           Object Detected: ${notification.object_detected}<br>
// //           Timestamp: ${notification.timestamp}<br>
// //           <img src="${notification.image_path}" alt="Detection Image" style="max-width: 100px;">
// //         `;
// //         notificationList.appendChild(li);
// //       });
// //     });
// // }

// function fetchDetectionNotifications() {
//   fetch('/detections')
//     .then(response => response.json())
//     .then(notifications => {
//       const detectionSelect = document.getElementById('detection-select');
//       detectionSelect.innerHTML = ''; // Clear the dropdown

//       notifications.forEach(notification => {
//         const option = document.createElement('option');
//         option.value = notification.id;
//         option.textContent = `Artifact ${notification.artifact_id} - ${notification.object_detected} - ${notification.timestamp}`;
//         detectionSelect.appendChild(option);
//       });

//       // Add an event listener to the dropdown
//       detectionSelect.addEventListener('change', () => {
//         const selectedNotificationId = detectionSelect.value;
//         fetchDetectionDetails(selectedNotificationId);
//       });
//     })
//     .catch(error => console.error('Error fetching detection notifications:', error));
// }

  
//   // Function to fetch predictive maintenance information
//   function fetchPredictiveMaintenance() {
//     // For now, let's simulate fetching predictive maintenance data
//     // You'll need to replace this with your actual API call
//     const artifactId = 1; // Replace with the actual artifact ID
//     fetch(`/maintenance/predict/${artifactId}`, { method: 'POST' })
//       .then(response => response.json())
//       .then(data => {
//         const prediction = data.prediction;
//         maintenanceInfo.innerHTML = `
//           <h3>Predictive Maintenance for Artifact ${artifactId}</h3>
//           <p>Risk Level: ${prediction.risk_level}</p>
//           <p>Predicted Failure Date: ${prediction.predicted_failure_date}</p>
//         `;
//       });
//   }
  
//   const sections = document.querySelectorAll('main > section');
//   sections.forEach(section => {
//     section.addEventListener('click', () => {
//       section.classList.toggle('fullscreen');
//     });
//   });


  // --- Socket.IO connection ---
  // socket.on('connect', () => {
  //   console.log('Connected to server');
  //   fetchArtifacts();
  //   fetchDetectionNotifications();
  //   fetchPredictiveMaintenance();
  // });

  // cameraSelect.addEventListener('change', () => {
  //   const selectCamera = cameraSelect.value;
  //   socket.emit('change_camera', selectCamera)
  // });
  // socket.emit('start_video')

  // socket.on('video_frame', (data) => {
  //     feedImage.src = `data:image/jpeg;base64,${data.frame}`;
  // });
    
// socket.on('frame0', (frameData) => {
//   feedImage0.src = 'data:image/jpeg;base64,' + frameData;
// });

// socket.on('frame1', (frameData) => {
//   feedImage1.src = 'data:image/jpeg;base64,' + frameData;
// });

// socket.on('alignment_result', (imageData) => {
//   alignmentResult.innerHTML = `<img src="data:image/jpeg;base64,${imageData}" alt=Alignment Result">`;
// })

// socket.on('alignment_error', (errorMessage) => {
//   alignmentResult.textContent = errorMessage;
// })