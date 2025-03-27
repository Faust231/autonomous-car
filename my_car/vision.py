# vision.py
"""
Module for vision processing.
Captures video frames from the Raspberry Pi camera and performs basic lane detection.
"""

import cv2
import numpy as np

class VisionProcessor:
    def __init__(self, camera_index=0):
        """
        Initialize the vision processor.
        :param camera_index: Index for cv2.VideoCapture (default is 0)
        """
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise IOError("Cannot open camera")

    def get_frame(self):
        """
        Capture a single frame from the camera.
        :return: frame (numpy array) or None if capture failed.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def process_frame(self, frame):
        """
        Process the frame to detect the white lane and calculate steering error.
        :param frame: input frame from camera
        :return: processed frame (for display) and error value (float)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        # Threshold to get white lanes (this might need tuning)
        _, thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)
        
        # Focus on region of interest (bottom half of the image)
        height, width = thresh.shape
        roi = thresh[int(height/2):, :]

        # Find contours in ROI
        contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        error = 0.0

        if contours:
            # Assume the largest contour is the lane marker
            largest_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                # Calculate error relative to the center of the ROI
                error = (cx - (width / 2)) / (width / 2)
                # Draw the contour and center line for visualization
                cv2.drawContours(roi, [largest_contour], -1, (255, 0, 0), 2)
                cv2.circle(roi, (cx, int(roi.shape[0]/2)), 5, (0, 0, 255), -1)
        else:
            print("No lane detected.")

        # For visualization, replace the ROI in the frame with processed ROI
        processed_frame = frame.copy()
        processed_frame[int(height/2):, :] = cv2.cvtColor_
