
# Chubaasiny Eswararao
# Date: 26th November 2024
# Title : Biometric Attendance System using Firebase Realtime Database

import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials, db, storage

# ----------------------------------------- Firebase Initialization ----------------------------------
# Initialize Firebase Admin SDK to connect to Firebase Realtime Database and Storage
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://attendancedatabase-fafa8-default-rtdb.firebaseio.com",
    'storageBucket': "attendancedatabase-fafa8.appspot.com"
})

# Importing student images
folderPath = 'Student Images'
pathList = os.listdir(folderPath)
print(pathList) #['SUKD2200111.png', 'SUKD2200222.png', 'SUKD2200333.png', 'SUKD2300111.png',
                # 'SUKD2300222.png', 'SUKD2300333.png', 'SUKD2300444.png']
imgStudentList = []
studentIds = []

for path in pathList:
    imgStudentList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])
    # print(os.path.splitext(path)[0]) #'SUKD2200111','.png'
    
    # Add images to Firebase storage 
    # refresh on Firebase storage page to view the update student images
    studentFileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(studentFileName)
    blob.upload_from_filename(studentFileName)

print(studentIds) # ['SUKD2200111', 'SUKD2200222', 'SUKD2200333', 'SUKD2300111', 'SUKD2300222', 
                    #'SUKD2300333', 'SUKD2300444']

def findEncodings(imgStudentList):
    encodeList = []
    for img in imgStudentList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    
    return encodeList

print("Encoding Started ... ")
encodeStudentList = findEncodings(imgStudentList)
encodeStudentListWithIds = [encodeStudentList, studentIds]
print("Encoding Complete ... ")

studentFile = open("EncodeStudentFile.p",'wb')

pickle.dump(encodeStudentListWithIds,studentFile)
studentFile.close()
print("File saved")

# Importing admin images
folderAdminPath = 'Admin Images'
adminPathList = os.listdir(folderAdminPath)
print(adminPathList)
imgAdminList = []
adminIds = []

for path in adminPathList:
    imgAdminList.append(cv2.imread(os.path.join(folderAdminPath,path)))
    adminIds.append(os.path.splitext(path)[0])

    # Add images to Firebase storage 
    # refresh on Firebase storage page to view the update admin images
    adminFileName = f'{folderAdminPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(adminFileName)
    blob.upload_from_filename(adminFileName)

print(adminIds) # 1 admin img

# Admin function
def findAdminEncodings(imgAdminList):
    encodeAdminList = []
    for adminImg in imgAdminList:
        adminImg = cv2.cvtColor(adminImg,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(adminImg)[0]
        encodeAdminList.append(encode)
    
    return encodeAdminList

print("Encoding Started ... ")
encodeAdminList = findEncodings(imgAdminList)
encodeAdminListWithIds = [encodeAdminList, adminIds]
print("Encoding Complete ... ")

# wb: write binary
adminFile = open("EncodeAdminFile.p",'wb') 

pickle.dump(encodeAdminListWithIds,adminFile)
adminFile.close()
print("File saved")
