const socket = io();
const feedImage = document.getElementById('feed-image');
const artifactList = document.getElementById('artifact-list').querySelector('ul');
const artifactDetails = document.getElementById('artifact-info');
const notificationList = document.getElementById('notification-list');
const maintenanceInfo = document.getElementById('maintenance-info');


function fetchArtifacts() {
    fetch('/artifacts')
        .then(response => response.json())
        .then(artifacts => {
            artifactList.innerHTML = ''; // Clear the list
            artifacts.forEach(artifact => {
                const li = document.createElement('li');
                li.textContent = artifact.name;
                li.addEventListener('click', () => {
                    fetchArtifactDetails(artifact.id);
                });
                artifactList.appendChild(li);
            });
        });
}

function fetchArtifactDetails(id) {
    fetch(`/artifacts/${id}`)
        .then(response => response.json())
        .then(artifact => {
            artifactDetails.innerHTML = ''; // Clear previous details
            const details = `
                <h3>${artifact.name}</h3>
                <p>${artifact.description}</p>
                <p>Status: ${artifact.status}</p>
                <img src="${artifact.image_path}" alt="${artifact.name}">
            `;
            artifactDetails.innerHTML = details;
        });
}

function fetchDetectionNotifications() {
  fetch('/detections')
    .then(response => response.json())
    .then(notifications => {
      notificationList.innerHTML = '';
      notifications.forEach(notification => {
        const li = document.createElement('li');
        li.innerHTML = `
          <strong>Artifact ID: ${notification.artifact_id}</strong><br>
          Object Detected: ${notification.object_detected}<br>
          Timestamp: ${notification.timestamp}<br>
          <img src="${notification.image_path}" alt="Detection Image" style="max-width: 100px;">
        `;
        notificationList.appendChild(li);
      });
    });
}

function fetchDetectionNotifications() {
  fetch('/detections')
    .then(response => response.json())
    .then(notifications => {
      const detectionSelect = document.getElementById('detection-select');
      detectionSelect.innerHTML = ''; // Clear the dropdown

      notifications.forEach(notification => {
        const option = document.createElement('option');
        option.value = notification.id;
        option.textContent = `Artifact ${notification.artifact_id} - ${notification.object_detected} - ${notification.timestamp}`;
        detectionSelect.appendChild(option);
      });

      // Add an event listener to the dropdown
      detectionSelect.addEventListener('change', () => {
        const selectedNotificationId = detectionSelect.value;
        fetchDetectionDetails(selectedNotificationId);
      });
    })
    .catch(error => console.error('Error fetching detection notifications:', error));
}

  
  // Function to fetch predictive maintenance information
  function fetchPredictiveMaintenance() {
    // For now, let's simulate fetching predictive maintenance data
    // You'll need to replace this with your actual API call
    const artifactId = 1; // Replace with the actual artifact ID
    fetch(`/maintenance/predict/${artifactId}`, { method: 'POST' })
      .then(response => response.json())
      .then(data => {
        const prediction = data.prediction;
        maintenanceInfo.innerHTML = `
          <h3>Predictive Maintenance for Artifact ${artifactId}</h3>
          <p>Risk Level: ${prediction.risk_level}</p>
          <p>Predicted Failure Date: ${prediction.predicted_failure_date}</p>
        `;
      });
  }
  
  const sections = document.querySelectorAll('main > section');
  sections.forEach(section => {
    section.addEventListener('click', () => {
      section.classList.toggle('fullscreen');
    });
  });

  // --- Socket.IO connection ---
  socket.on('connect', () => {
    console.log('Connected to server');
    fetchArtifacts();
    fetchDetectionNotifications();
    fetchPredictiveMaintenance();
  });

socket.on('frame', (frameData) => {
    feedImage.src = 'data:image/jpeg;base64,' + frameData;
});