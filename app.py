from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import cv2
import base64
import numpy as np

app = Flask(__name__, template_folder="templates", static_folder="../static")
app.config['SECRET_KEY'] = "@12345"
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.start_background_task(target=capture_and_send_frames)

def capture_and_send_frames():
    camera = cv2.VideoCapture(0)  # Use 1 for the external USB camera
    if not camera.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        # Encode the frame
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = base64.b64encode(buffer).decode('utf-8')

        # Emit the frame data to the client
        socketio.emit('frame', frame_data)

        socketio.sleep(0.05)  # Adjust the delay as needed

    camera.release()

if __name__ == '__main__':
    socketio.run(app, debug=True)