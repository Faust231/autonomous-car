# telemetry.py
"""
Module for telemetry data reading using pyserial.
Reads data from the Telemetry Expander 2.0 TDi via UART.
"""

import serial

class TelemetryReader:
    def __init__(self, port='/dev/ttyS0', baudrate=9600, timeout=1):
        """
        Initialize the telemetry reader.
        :param port: Serial port (default '/dev/ttyS0')
        :param baudrate: Baud rate (default 9600)
        :param timeout: Read timeout in seconds.
        """
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            print(f"Opened serial port {port} at {baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.ser = None

    def read_line(self):
        """
        Read a line of telemetry data.
        :return: Decoded string from telemetry data or None if no data.
        """
        if self.ser and self.ser.in_waiting:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                return line
            except Exception as e:
                print(f"Error reading telemetry: {e}")
                return None
        return None

    def close(self):
        """
        Close the serial port.
        """
        if self.ser:
            self.ser.close()
            print("Serial port closed.")
