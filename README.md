# AttendEase - Face Recognition Attendance System

## Overview
This project is **AttendEase**, a **Face Recognition Attendance System** developed using Python, OpenCV, and Firebase. It allows students to log their attendance by scanning their faces, and admins can view attendance records and generate reports.

## Features
- **Student Authentication:** Uses face recognition to verify student identity and log attendance.
- **Admin Access:** Admins can log in via face recognition and view attendance records.
- **Database Integration:** Attendance records are stored and retrieved from Firebase.
- **Real-Time Data Processing:** Updates attendance data in real-time.
- **Report Generation:** Exports attendance data in XML and PDF formats.

## Technologies Used
- **Python** (Face Recognition, OpenCV, Firebase Admin SDK)
- **Firebase** (Realtime Database, Storage)
- **Google Sheets** (Attendance record viewing)
- **Tkinter** (User Interface for role selection)
- **HTML/CSS** (Admin Dashboard UI)

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- OpenCV (`pip install opencv-python`)
- Face Recognition (`pip install face-recognition`)
- Firebase Admin SDK (`pip install firebase-admin`)
- Numpy (`pip install numpy`)
- Tkinter (Included with Python)

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/AttendEase.git
   cd AttendEase
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up Firebase:
   - Create a Firebase project and enable Realtime Database & Storage.
   - Download the `serviceAccountKey.json` and place it in the project folder.
4. Run the program:
   ```sh
   python role_selection.py
   ```

## Usage
1. **Students**
   - Click on "Student" to start face recognition.
   - Show your face in front of the webcam.
   - If recognized, attendance is logged in Firebase.
   - If scanned again within 2 hours, it will show "Attendance Already Taken".

2. **Admins**
   - Click on "Admin" and log in using face recognition.
   - The system will open the admin dashboard.
   - View attendance records and download reports.

## File Structure
```
AttendEase/
│-- role_selection.py  # UI for role selection
│-- main.py            # Student face recognition
│-- adminmain.py       # Admin face recognition
│-- AddingDataToDb.py  # Adds student/admin data to Firebase
│-- EncodeGenerator.py # Generates face encodings
│-- admin.html         # Admin dashboard UI
│-- requirements.txt   # Dependencies
│-- serviceAccountKey.json  # Firebase credentials
│-- Student Images/    # Folder for student face images
│-- Admin Images/      # Folder for admin face images
```
