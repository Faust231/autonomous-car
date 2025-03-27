# tests/test_pwm.py
"""
Test script for PWM control using pwm_control.py.
Cycles through a series of PWM pulsewidth values for both steering and motor.
"""

import time
from pwm_control import PWMController

def test_pwm_cycle():
    # Example GPIO pins for testing; update these to match your setup.
    STEERING_PIN = 17
    MOTOR_PIN = 18

    pwm = PWMController(steering_pin=STEERING_PIN, motor_pin=MOTOR_PIN)
    
    try:
        # Test a cycle for the steering signal: left, center, right, center, left.
        pwm_values = [1000, 1500, 2000, 1500, 1000]
        for val in pwm_values:
            print(f"Setting steering PWM to {val} µs")
            pwm.set_steering(val)
            time.sleep(1)  # Wait 1 second between values
        
        # Test a cycle for the motor signal: from stop to full throttle and back.
        pwm_values_motor = [1000, 1250, 1500, 1750, 2000, 1750, 1500, 1250, 1000]
        for val in pwm_values_motor:
            print(f"Setting motor PWM to {val} µs")
            pwm.set_motor(val)
            time.sleep(1)
    except KeyboardInterrupt:
        print("PWM test interrupted.")
    finally:
        pwm.stop()
        pwm.cleanup()

if __name__ == '__main__':
    test_pwm_cycle()
