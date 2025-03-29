
# Chubaasiny Eswararao
# Date: 26th November 2024
# Title : Biometric Attendance System using Firebase Realtime Database

import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials, db, storage
import time
from datetime import datetime

# ----------------------------------------- Firebase Initialization ----------------------------------
# Initialize Firebase Admin SDK to connect to Firebase Realtime Database and Storage
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendancedatabase-fafa8-default-rtdb.firebaseio.com/",
    'storageBucket': "attendancedatabase-fafa8.appspot.com"
})

bucket = storage.bucket()

# --------------------------------- Open Video Capture and Set up Settings ---------------------------
# Open webcam for live video feed
capture = cv2.VideoCapture(0)
capture.set(3, 640)     # Set the width of the capture window
capture.set(4, 480)     # Set the height of the capture window

# Load background image for User Interface
backgroundImg = cv2.imread('Resources/Background.png')

# Load mode images from the 'Resources/Modes' folder for different display modes
folderModePath = 'Resources/Modes'
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in os.listdir(folderModePath)]

# ------------------------------------ Load Student Encodings ----------------------------------------
# Load the pre-encoded face data (students' images and IDs) from a pickled file
with open('EncodeStudentFile.p', 'rb') as studentFile:
    encodeStudentListWithIds = pickle.load(studentFile)
encodeStudentList, studentIds = encodeStudentListWithIds

# --------------------------------------- Global Variables -------------------------------------------
# Global variables
modeType = 0
last_scanned_id = None
last_scanned_time = None
studentImg = []

# ----------------------------------- Main Face Detection Loop ---------------------------------------
while True:
    # Capture a frame from the webcam
    success, img = capture.read()
    if not success:
        continue
    
    # Resize the image and convert it from BGR to RGB
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces in the current frame
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    # Place the captured video on the background image at specified coordinates
    backgroundImg[163:163 + 480, 55:55 + 640] = img
    backgroundImg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    # If faces are detected, proceed with face recognition
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            # Compare the detected face with pre-encoded students' images
            matches = face_recognition.compare_faces(encodeStudentList, encodeFace)
            faceDis = face_recognition.face_distance(encodeStudentList, encodeFace)
            matchIndex = np.argmin(faceDis)

            # If student matches, process the identified student
            if matches[matchIndex]:
                current_id = studentIds[matchIndex]
                current_time = datetime.now()

                # Print the detected student ID , login data and time
                print("Known Face Detected")
                print(f"Student ID: {current_id}, Time: {current_time}")

                # Get the bounding box of the face and draw a green rectangle around detected face
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4     # Rescale to original size
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1      # bbox includes x, y, width, height
                backgroundImg = cvzone.cornerRect(backgroundImg, bbox, rt=0)

                # Check if the same student was scanned recently
                if last_scanned_id == current_id and last_scanned_time:
                    # Calculate the time difference between the current scan and the last scan
                    time_elapsed = (current_time - last_scanned_time).total_seconds()
                    
                    # If less than 2 hours (7200 seconds) have passed since the last scan, skip taking attendance 
                    if time_elapsed < 7200:
                        # Switch to Mode 3: Display a message indicating attendance already taken
                        modeType = 3 
                        # Log the time elapsed and indicate why the attendance cannot be taken again
                        print('Attendance already taken recently.')
                        print(f'Time elapsed since last scan: {time_elapsed:.2f} seconds')
                        print('Please wait for 2 hours before next scanning.')
                        
                        # Break from the loop and skip further processing for this scan
                        break  # Skip further attendance processing for this scan

                # Update the scanned time and ID
                last_scanned_id = current_id
                last_scanned_time = current_time

                # Fetch student details and and image from Firebase
                studentInfo = db.reference(f'Students/{current_id}').get()
                blob = bucket.get_blob(f'Student Images/{current_id}.png') # Fetch the student image
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                studentImg = cv2.imdecode(array, cv2.IMREAD_COLOR)  # Decode image as OpenCV format

                # Update the student's attendance in Firebase
                datetimeObject = datetime.strptime(studentInfo['last_attendance_taken'], "%Y-%m-%d %H:%M:%S")
                timeInSecsElapsed = (current_time - datetimeObject).total_seconds()

                # If more than 7200seconds(2hours) have passed since the last attendance, update attendance count
                if timeInSecsElapsed > 7200: 
                    students_ref = db.reference(f'Students/{current_id}')
                    studentInfo['total_attendance'] += 1
                    students_ref.child('total_attendance').set(studentInfo['total_attendance'])
                    students_ref.child('last_attendance_taken').set(current_time.strftime("%Y-%m-%d %H:%M:%S"))
                    print('Attendance taken again.')

                # Switch to Mode 1: Display student information for 5 seconds
                modeType = 1 
                start_time = time.time()  # Start timer for 5 seconds

                # Display student info on the screen for 5 seconds
                while time.time() - start_time < 5:
                    backgroundImg[44:44 + 633, 808:808 + 414] = imgModeList[modeType] # Set background for Mode 1
                    # Display student's total attendance, ID, and major
                    cv2.putText(backgroundImg, str(studentInfo['total_attendance']), (820, 125),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                    cv2.putText(backgroundImg, str(studentInfo['student_id']), (980, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(backgroundImg, str(studentInfo['major']), (980, 548),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    # Display the student's name centered of the screen
                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(backgroundImg, str(studentInfo['name']), (808 + offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (25, 25, 25), 1)

                    # Display the student's image
                    studentImg_resized = cv2.resize(studentImg, (216, 216))
                    backgroundImg[175:175 + 216, 909:909 + 216] = studentImg_resized

                    # Show updated UI
                    cv2.imshow("Face Attendance", backgroundImg) 
                    cv2.waitKey(1)  # Non-blocking wait to show images

                # Switch to modeType 2 after displaying modeType1 for 5 seconds
                modeType = 2
                
                # Display Mode 2 for 5 seconds
                start_time = time.time()
                while time.time() - start_time < 5:
                    print(modeType)
                    print(time.time() - start_time)

                    backgroundImg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                    cv2.imshow("Face Attendance", backgroundImg)
                    cv2.waitKey(1)  # Non-blocking wait to show images

                # Reset for next scan: Clear student image
                studentImg = []  

    else:
        # If no face is detected, stay in default mode (modeType 0)
        modeType = 0  
    
    # Display the final frame with updated information
    cv2.imshow("Face Attendance", backgroundImg)
    cv2.waitKey(1)     # Non-blocking wait to show the updated image
