# webapp.py
"""
Flask web application to provide a web interface for the RC car.
Serves a video feed and displays telemetry data.
"""

from flask import Flask, render_template, Response, request
import cv2
import threading
import time

# Global variable to store the latest frame
global_frame = None
frame_lock = threading.Lock()

app = Flask(__name__)

@app.route('/')
def index():
    """
    Home page that displays the video feed and telemetry.
    """
    return render_template('index.html')

def generate_frames():
    """
    Generator function that yields video frames in MJPEG format.
    """
    global global_frame, frame_lock
    while True:
        with frame_lock:
            if global_frame is None:
                continue
            ret, buffer = cv2.imencode('.jpg', global_frame)
            frame = buffer.tobytes()
        # Yield the frame in HTTP multipart format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.1)

@app.route('/video_feed')
def video_feed():
    """
    Route to return the video feed.
    """
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Dummy telemetry endpoint for demonstration.
@app.route('/telemetry')
def telemetry():
    telemetry_data = {"rpm": 0}  # Replace with actual data as needed.
    return telemetry_data

# Endpoint for manual PWM override (for testing purposes)
@app.route('/update_pwm', methods=['POST'])
def update_pwm():
    steering = request.form.get('steering')
    motor = request.form.get('motor')
    print(f"Manual override - Steering: {steering}, Motor: {motor}")
    return "PWM updated", 200
