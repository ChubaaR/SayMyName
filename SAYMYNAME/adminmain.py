
# Chubaasiny Eswararao
# Date: 26th November 2024
# Title : Biometric Attendance System using Firebase Realtime Database

import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import webbrowser
import firebase_admin
from firebase_admin import credentials, db, storage
import threading
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

# ------------------------------------ Open Video Capture and Set up Settings ------------------------
# Open webcam for live video feed
capture = cv2.VideoCapture(0)
capture.set(3, 640)     # Set the width of the capture window
capture.set(4, 480)     # Set the height of the capture window

# Load background image for User Interface
backgroundImg = cv2.imread('Resources/Background.png')

# Load mode images from the 'Resources/Modes' folder for different display modes
folderModePath = 'Resources/Modes'
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in os.listdir(folderModePath)]

# ------------------------------------ Load Admin Encodings ------------------------------------------
# Load the pre-encoded face data (admin image and ID) from a pickled file
with open('EncodeAdminFile.p', 'rb') as adminFile:
    encodeAdminListWithIds = pickle.load(adminFile)
encodeAdminList, adminIds = encodeAdminListWithIds

# ---------------------------------------- Global Variables ------------------------------------------
# Global variables
modeType = 0  
last_scanned_id = None
last_scanned_time = None
adminImg = []

# --------------------------------------- Open Browser Function --------------------------------------
def open_browser():
    # Function to open a specify admin page in Microsoft Edge browser 
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))
    webbrowser.get('edge').open('file:///D:/Downloads/ATTENDEASE/ATTENDEASE/admin.html')

# ----------------------------------- Main Face Detection Loop ---------------------------------------
while True:
    # Capture a frame from the webcam
    success, img = capture.read()
    if not success:
        continue
    
    # Resize the image and convert it from BGR to RGB
    imgA = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgA = cv2.cvtColor(imgA, cv2.COLOR_BGR2RGB)

    # Detect faces in the current frame
    faceCurFrame = face_recognition.face_locations(imgA)
    encodeCurFrame = face_recognition.face_encodings(imgA, faceCurFrame)

    # Place the captured video on the background image at specified coordinates
    backgroundImg[163:163 + 480, 55:55 + 640] = img
    backgroundImg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    # If faces are detected, proceed with face recognition
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            # Compare the detected face with pre-encoded admin faces
            matches = face_recognition.compare_faces(encodeAdminList, encodeFace)
            faceDis = face_recognition.face_distance(encodeAdminList, encodeFace)
            matchIndex = np.argmin(faceDis)
           
            # If admin matches, process the identified admin
            if matches[matchIndex]:
                current_id = adminIds[matchIndex]
                current_time = datetime.now()
               
                # Print the detected admin ID , login date and time
                print("Known Admin Face Detected")
                print(f"Admin ID: {current_id}, Time: {current_time}")

                # Get the bounding box of the face and draw a green rectangle around detected face
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4     # Rescale to original size
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1      # bbox includes x:width, y:height
                backgroundImg = cvzone.cornerRect(backgroundImg, bbox, rt=0)
               
                # Update the scanned ID and time
                last_scanned_id = current_id
                last_scanned_time = current_time

                # Fetch admin details and and image from Firebase
                adminInfo = db.reference(f'Admin/{current_id}').get()
                blob = bucket.get_blob(f'Admin Images/{current_id}.png') # Fetch the admin image
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                adminImg = cv2.imdecode(array, cv2.IMREAD_COLOR)    # Decode image as OpenCV format

                # Update the 'last_login_time' field in Firebase for the detected admin
                admin_ref = db.reference(f'Admin/{current_id}')
                admin_ref.child('last_login_time').set(current_time.strftime("%Y-%m-%d %H:%M:%S"))

                # Change to modeType 4 (admin info display mode)
                modeType = 4
                start_time = time.time()  # Start timer for 5 seconds to show admin details
                
                # Display admin information and image for 5 seconds before opening the browser
                while time.time() - start_time < 5:
                    # print(time.time() - start_time)
                    print(f"Time elapsed: {time.time() - start_time:.2f}s")
                    backgroundImg[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    # Display admin name and ID on the screen
                    cv2.putText(backgroundImg, str(adminInfo['name']), (980, 493),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(backgroundImg, str(adminInfo['admin_id']), (980, 548),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)

                    # Display admin image
                    adminImg_resized = cv2.resize(adminImg, (216, 216))
                    backgroundImg[175:175 + 216, 909:909 + 216] = adminImg_resized

                    # Show the updated UI
                    cv2.imshow("Face Attendance", backgroundImg)
                    cv2.waitKey(1)  # Non-blocking wait to show images

                # Open the browser in a separate thread
                threading.Thread(target=open_browser).start()
               
                # Reset for next scan: Clear admin image
                adminImg = []  

    else:
        # If no face is detected, stay in default mode (modeType 0)
        modeType = 0

    # Display the final frame with updated information
    cv2.imshow("Face Attendance", backgroundImg)
    cv2.waitKey(1) # Non-blocking wait to show the updated image

