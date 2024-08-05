import numpy as np
import cv2
import speech_recognition as sr
import threading
from pyzbar.pyzbar import decode
import webbrowser

def video():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def detect_faces():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def detect_emotions():
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    previous_emotion = "neutral"
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        emotion_detected = "neutral"
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
            if len(smiles) > 0:
                emotion_detected = "happy"
                for (sx, sy, sw, sh) in smiles:
                    cv2.rectangle(frame[y:y+h, x:x+w], (sx, sy), (sx + sw, sy + sh), (0, 255, 255), 2)
        if emotion_detected != previous_emotion:
            if emotion_detected == "happy":
                message = "You seem very happy today!"
            else:
                message = "You seem neutral or not smiling today."
            print(message)
            previous_emotion = emotion_detected
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def detect_colors():
    webcam = cv2.VideoCapture(0)
    while True:
        _, imageFrame = webcam.read()
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        red_lower = np.array([136, 87, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

        green_lower = np.array([25, 52, 72], np.uint8)
        green_upper = np.array([102, 255, 255], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

        blue_lower = np.array([94, 80, 2], np.uint8)
        blue_upper = np.array([120, 255, 255], np.uint8)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

        kernel = np.ones((5, 5), "uint8")

        red_mask = cv2.dilate(red_mask, kernel)
        res_red = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask)

        green_mask = cv2.dilate(green_mask, kernel)
        res_green = cv2.bitwise_and(imageFrame, imageFrame, mask=green_mask)

        blue_mask = cv2.dilate(blue_mask, kernel)
        res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask=blue_mask)

        contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(imageFrame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

        contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(imageFrame, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))

        contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > 300:
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(imageFrame, "Blue Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))

        cv2.imshow("Multiple Color Detection in Real-Time", imageFrame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    webcam.release()
    cv2.destroyAllWindows()

def reader():
    # Initialize the video capture device
    captureDevice = cv2.VideoCapture(0)
    captureDevice.set(3, 640)  # Set the frame width
    captureDevice.set(4, 480)  # Set the frame height

    # To keep track of scanned QR codes
    scanned_data = set()
    webcam = cv2.VideoCapture(0)
    try:
        while True:
            # Read a frame from the capture device
            success, image = captureDevice.read()
            if not success:
                print("Failed to capture image")
                break

            # Display the live video feed
            cv2.imshow('Live Camera Capture', image)
            
            # Decode QR codes in the image
            decoded_objects = decode(image)
            for obj in decoded_objects:
                data = obj.data.decode('utf-8')
                if data not in scanned_data:
                    scanned_data.add(data)
                    print('Scanning: ' + data)
                    webbrowser.open(data)  # Open the link in the default web browser

            # Check for key press and exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Exiting...")
                break
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        # Release the capture device and close any OpenCV windows
        captureDevice.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    user_input = input("Enter 'face detection', 'emotion detection', 'color detection', 'video', or 'qr reader': ")
    print("press q to quit")
    if user_input == "face detection":
        detect_faces()
    elif user_input == "emotion detection":
        detect_emotions()
    elif user_input == "color detection":
        detect_colors()
    elif user_input == "video":
        video()
    elif user_input == "qr reader":
        reader()
    else:
        print("Invalid input. Please try again.")
