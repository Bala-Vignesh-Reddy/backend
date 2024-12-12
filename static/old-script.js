const feedImage = document.getElementById('feed-image');
const artifactList = document.getElementById('artifact-list').querySelector('ul');
const artifactDetails = document.getElementById('detection-info');
const notificationList = document.getElementById('notifications').querySelector('ul');
const maintenanceInfo = document.getElementById('maintenance-info');

// Function to fetch artifacts from the API
function fetchArtifacts() {
  fetch('/artifacts')
    .then(response => response.json())
    .then(artifacts => {
      artifactList.innerHTML = '';
      artifacts.forEach(artifact => {
        const li = document.createElement('li');
        li.textContent = artifact.name;
        li.addEventListener('click', () => {
          fetchArtifactDetails(artifact.id);
        });
        artifactList.appendChild(li);
      });
    })
    .catch(error => console.error('Error fetching artifacts:', error));
}

// Function to fetch artifact details
function fetchArtifactDetails(id) {
  fetch(`/artifacts/${id}`)
    .then(response => response.json())
    .then(artifact => {
      artifactDetails.innerHTML = '';
      const details = `
                <h3>${artifact.name}</h3>
                <p>${artifact.description}</p>
                <p>Status: ${artifact.status}</p>
                <img src="${artifact.image_path}" alt="${artifact.name}" style="max-width: 100%;">
            `;
      artifactDetails.innerHTML = details;
    })
    .catch(error => console.error('Error fetching artifact details:', error));
}

// Function to fetch detection notifications
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

// Function to fetch and display details for a specific detection
function fetchDetectionDetails(notificationId) {
  fetch(`/detections/${notificationId}`)
    .then(response => response.json())
    .then(notification => {
      artifactDetails.innerHTML = '';
      const details = `
        <h3>Detection Details</h3>
        <p>Artifact ID: ${notification.artifact_id}</p>
        <p>Object Detected: ${notification.object_detected}</p>
        <p>Timestamp: ${notification.timestamp}</p>
        <img src="${notification.image_path}" alt="Detection Image" style="max-width: 100%;">
      `;
      artifactDetails.innerHTML = details;
    })
    .catch(error => console.error('Error fetching detection details:', error));
}

// Function to fetch predictive maintenance information
function fetchPredictiveMaintenance() {
  // For now, let's simulate fetching predictive maintenance data
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
    })
    .catch(error => console.error('Error fetching predictive maintenance info:', error));
}

// --- Full-screen functionality ---
const sections = document.querySelectorAll('main > section');

sections.forEach(section => {
  const closeButton = section.querySelector('.close-button');
  closeButton.addEventListener('click', () => {
    section.classList.remove('fullscreen');
  });

  section.addEventListener('click', (event) => {
    // Check if the click target is the close button
    if (event.target === closeButton) {
      return; // Don't toggle fullscreen if the close button is clicked
    }
    section.classList.toggle('fullscreen');
  });
});


// Function to display the video feed
var videoElement = document.getElementById('video');
function reloadVideoFeed() {
    videoElement.src = "{{ url_for('video_feed') }}" + "?rand=" + new Date().getTime();
}
reloadVideoFeed()
document.addEventListener("visibilitychange", function() {
    if(document.visibilityState === "visible"){
        reloadVideoFeed()
    }
})


// Call the functions to fetch and display data when the page loads
document.addEventListener('DOMContentLoaded', () => {
  fetchArtifacts();
  fetchDetectionNotifications();
  fetchPredictiveMaintenance();
//   reloadVideoFeed();
});