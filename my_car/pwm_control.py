# pwm_control.py
"""
Module for controlling PWM signals using pigpio.
Provides functionality to control the steering servo and motor ESC.
"""

import pigpio
import time

class PWMController:
    def __init__(self, steering_pin, motor_pin, frequency=50):
        """
        Initialize PWM controller.
        :param steering_pin: GPIO pin for steering servo
        :param motor_pin: GPIO pin for motor ESC
        :param frequency: PWM frequency in Hz (default is 50Hz for servos)
        """
        self.steering_pin = steering_pin
        self.motor_pin = motor_pin
        self.frequency = frequency
        self.pi = pigpio.pi()
        if not self.pi.connected:
            raise IOError("Could not connect to pigpio daemon!")
        
        # Set frequency for the pins
        self.pi.set_PWM_frequency(self.steering_pin, self.frequency)
        self.pi.set_PWM_frequency(self.motor_pin, self.frequency)

    def set_steering(self, pulsewidth):
        """
        Set the steering servo pulsewidth in microseconds.
        Typical range: 1000 (rechts) to 2000 (links), with 1500 as mitte.
        :param pulsewidth: Pulsewidth in microseconds.
        """
        self.pi.set_servo_pulsewidth(self.steering_pin, pulsewidth)
        # Debug print
        print(f"Steering PWM set to {pulsewidth}µs on pin {self.steering_pin}")

    def set_motor(self, pulsewidth):
        """
        Set the motor ESC pulsewidth in microseconds.
        Typical range: 1000 (backwards) to 1500 (stop) to 2000 (full throttle).
        :param pulsewidth: Pulsewidth in microseconds.
        """
        self.pi.set_servo_pulsewidth(self.motor_pin, pulsewidth)
        # Debug print
        print(f"Motor PWM set to {pulsewidth}µs on pin {self.motor_pin}")

    def stop(self):
        """
        Stop PWM signals on both channels.
        """
        self.pi.set_servo_pulsewidth(self.steering_pin, 0)
        self.pi.set_servo_pulsewidth(self.motor_pin, 0)
        print("PWM signals stopped.")

    def cleanup(self):
        """
        Clean up the pigpio connection.
        """
        self.pi.stop()
        print("Pigpio connection closed.")
