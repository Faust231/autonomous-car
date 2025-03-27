# main.py
"""
Main application file to integrate vision processing, PWM control, telemetry, and web interface.
"""

import threading
import time

from pwm_control import PWMController
from vision import VisionProcessor
from telemetry import TelemetryReader
from webapp import app, frame_lock, global_frame

# Constants for default PWM values
PWM_STEERING_CENTER = 1500  # µs
PWM_MOTOR_STOP = 1000       # µs (adjust as necessary)

def web_server():
    """Start the Flask web server."""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def vision_loop(vision_processor, pwm_controller):
    """Capture and process video frames, adjust PWM signals based on lane detection."""
    global global_frame, frame_lock

    try:
        while True:
            frame = vision_processor.get_frame()
            if frame is None:
                continue

            processed_frame, error = vision_processor.process_frame(frame)
            
            # Update global frame for the web interface
            with frame_lock:
                global_frame = processed_frame.copy()
            
            # Calculate PWM adjustments based on error.
            # Here we use a simple proportional control: error in the range -1 to 1
            steering_pwm = PWM_STEERING_CENTER + int(error * 100)  # Adjust gain as necessary.
            # Clamp PWM to a safe range (1000-2000 µs)
            steering_pwm = max(1000, min(2000, steering_pwm))
            
            # For motor control, we simply set a constant throttle here.
            motor_pwm = PWM_MOTOR_STOP

            # Set PWM signals
            pwm_controller.set_steering(steering_pwm)
            pwm_controller.set_motor(motor_pwm)
            
            print(f"Lane error: {error:.2f}, Steering PWM: {steering_pwm}, Motor PWM: {motor_pwm}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Vision loop interrupted. Exiting...")

def telemetry_loop(telemetry_reader):
    """Continuously read telemetry data and print it."""
    try:
        while True:
            data = telemetry_reader.read_line()
            if data:
                print("Telemetry:", data)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Telemetry loop interrupted. Exiting...")

def main():
    # Initialize PWM controller (update GPIO pins as needed)
    STEERING_PIN = 17  # Example GPIO pin number
    MOTOR_PIN = 18     # Example GPIO pin number
    pwm_controller = PWMController(steering_pin=STEERING_PIN, motor_pin=MOTOR_PIN)
    
    # Initialize vision processor (camera index 0)
    vision_processor = VisionProcessor(camera_index=0)

    # Initialize telemetry reader (update serial port as necessary)
    telemetry_reader = TelemetryReader(port='/dev/ttyS0', baudrate=9600)

    # Start the web server in a separate thread
    web_thread = threading.Thread(target=web_server, daemon=True)
    web_thread.start()
    print("Web server started at http://0.0.0.0:5000")

    # Start telemetry reading in a separate thread
    telemetry_thread = threading.Thread(target=telemetry_loop, args=(telemetry_reader,), daemon=True)
    telemetry_thread.start()

    # Start vision processing loop in the main thread
    try:
        vision_loop(vision_processor, pwm_controller)
    finally:
        # Cleanup resources on exit
        vision_processor.release()
        telemetry_reader.close()
        pwm_controller.stop()
        pwm_controller.cleanup()

if __name__ == '__main__':
    main()
