
# Chubaasiny Eswararao
# Date: 26th November 2024
# Title : Biometric Attendance System using Firebase Realtime Database


import firebase_admin
from firebase_admin import credentials
from firebase_admin import db   

# ----------------------------------------- Firebase Initialization ----------------------------------
# Initialize Firebase Admin SDK to connect to Firebase Realtime Database
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : "https://attendancedatabase-fafa8-default-rtdb.firebaseio.com/" #database might get expired
})

# Students' reference (Realtime Database)
students_ref = db.reference("Students")

# Define student data
students_data = {
    "SUKD2200111": # key 
    {
        # Value
        "name" : "Angelina Jolie",
        "student_id": "SUKD2200111",
        "major" : "Computer Science",
        "last_attendance_taken" : "2024-01-26 16:10:30",
        "total_attendance" : 3,
    },
    "SUKD2200222": # key
    {
        # Value
        "name" : "Lee Chong Wei",
        "student_id": "SUKD2200222",
        "major" : "Accounting",
        "last_attendance_taken" : "2023-09-15 17:30:30",
        "total_attendance" : 4,
    },
    "SUKD2200333": # key
    {
        # Value
        "name" : "Elon Musk",
        "student_id": "SUKD2200333",
        "major" : "Business",
        "last_attendance_taken" : "2024-01-22 01:30:30",
        "total_attendance" : 2,
    },
    "SUKD2300111": # key
    {
        # Value
        "name" : "John Legend",
        "student_id": "SUKD2300111",
        "major" : "MBBS",
        "last_attendance_taken" : "2024-01-22 01:30:30",
        "total_attendance" : 5,
    },
    "SUKD2300222": # key
    {
        # Value
        "name" : "Kendall Jenner",
        "student_id": "SUKD2300222",
        "major" : "Pharmacy",
        "last_attendance_taken" : "2024-01-22 01:30:30",
        "total_attendance" : 2,
    },
    "SUKD2300333": # key
    {
        # Value
        "name" : "Karina",
        "student_id": "SUKD2300333",
        "major" : "Psychology",
        "last_attendance_taken" : "2024-01-22 01:30:30",
        "total_attendance" : 3,
    },
    "SUKD2300444": # key
    {
        # Value
        "name" : "Sana",
        "student_id": "SUKD2300444",
        "major" : "Optometry",
        "last_attendance_taken" : "2024-10-06 01:30:30",
        "total_attendance" : 2,
    },
}

# Store students' data in Firebase
for key, value in students_data.items():
    students_ref.child(key).update(value) # Use update(can update) instead of set(can't update)

# Admins' reference (Realtime Database)
admin_ref = db.reference("Admin")

# Define admin data
admin_data = {
    "ADMIN22222": # Key
    {
        # Value
        "name" : "David",
        "admin_id" : "ADMIN22222",
        "last_login_time" : "2024-11-26 20:10:30",
    },
}

# Store admin data in Firebase
for key, value in admin_data.items():
    admin_ref.child(key).update(value)
