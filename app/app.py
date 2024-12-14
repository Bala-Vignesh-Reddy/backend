# from flask import Flask, render_template
# from flask_socketio import SocketIO, emit
# import cv2
# import base64
# import numpy as np
# import threading

# app = Flask(__name__, template_folder="templates", static_folder="../static")
# app.config['SECRET_KEY'] = "@12345"
# socketio = SocketIO(app)

# camera_thread = None  # Initialize camera_thread

# @app.route('/')
# def index():
#     return render_template('index.html')

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected')
#     global camera_thread
#     camera_thread = threading.Thread(target=capture_and_send_frames, args=('frame0',))
#     camera_thread.start()

# @socketio.on('change_camera')
# def handle_change_camera(event_name):
#     global camera_thread

#     if camera_thread is not None and camera_thread.is_alive():
#         camera_thread.join()

#     camera_thread = threading.Thread(target=capture_and_send_frames, args=(event_name,))
#     camera_thread.start()

# def capture_and_send_frames(event_name):
#     camera_index = 0 if event_name == 'frame0' else 1
#     camera = cv2.VideoCapture(camera_index)
#     if not camera.isOpened():
#         raise IOError(f"Cannot open webcam {camera_index}")

#     try:
#         while True:
#             ret, frame = camera.read()
#             if not ret:
#                 break

#             _, buffer = cv2.imencode('.jpg', frame)
#             frame_data = base64.b64encode(buffer).decode('utf-8')

#             socketio.emit(event_name, frame_data)
#             socketio.sleep(0.05)
#     finally:
#         camera.release()

# if __name__ == '__main__':
#     socketio.run(app, debug=True)

from flask import Flask, render_template, Response, jsonify
import cv2
from app.api import detections, artifacts, maintenance
import datetime 
import torch
import numpy as np

app = Flask(__name__, template_folder='templates', static_folder="../static")

app.register_blueprint(artifacts.bp)
app.register_blueprint(detections.bp)
app.register_blueprint(maintenance.bp)

active_feature = 'live_feed'
models = {}

def live_feed():
    camera = cv2.VideoCapture(0)  # Default camera
    if not camera.isOpened():
        print("Error: could not access the camera.")
        return 
    
    while True:
        # Read a frame from the camera
        success, frame = camera.read()
        if not success:
            print("Error: Failed to capture frame.")
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Failed to encode frame.")
                break
            frame = buffer.tobytes()

            # Yield the frame as part of a multipart stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Release the camera when done
    camera.release()    

def gen_frames():
    # model = torch.hub.load('ultralytics/yolov5', 'yolov5n', pretrained=True)
    camera = cv2.VideoCapture(0)
    path = "models/display.pt"
    model = None

    model = torch.hub.load('ultralytics/yolov5', 'custom', path=path,  force_reload=True)
    model.eval()
    if not camera.isOpened():
        print("Error: Could not access the camera.")
        return
    while True:
        success, frame = camera.read()
        if not success:
            print("Error: Failed to capture frame.")
            break
        else:
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Error: Failed to encode frame.")
                break
            frame = buffer.tobytes()

            # Yield the frame as part of a multipart stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/warnings')
def get_warnings():
    # Replace this with your actual logic to fetch warnings
    warnings = [
        {
            'message': 'Anomaly detected!',
            'location': 'Exhibit A',
            'timestamp': '2024-12-14 10:00:00'
        }
    ]
    return jsonify(warnings)

@app.route('/api/proximity_alerts')
def get_proximity_alerts():
    alerts = [{
        'message' : 'Proximity alert triggered!',
        'location' : 'Entrance',
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }]
    return jsonify(alerts)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)
