
# Chubaasiny Eswararao
# Date: 26th November 2024
# Title : Biometric Attendance System using Firebase Realtime Database

import tkinter as tk
from tkinter import messagebox
import subprocess
from PIL import Image, ImageTk
import os

# Create the main window
root = tk.Tk()
root.title("Role Selection")
root.geometry("800x550")
root.configure(bg="#f0f8ff")

# Function for student button
def open_student():
    try:
        subprocess.run(["python", "main.py"])  # Runs main.py
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open main.py: {e}")

# Function for admin button
def open_admin():
    try:
        subprocess.run(["python", "adminmain.py"])  # Runs adminmain.py
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open adminmain.py: {e}")

# Create the header
header = tk.Frame(root, bg="white", height=90)
header.pack(fill="x")
header.pack_propagate(False)

# Logo Path (make sure it's correct)
logo_path = r'D:\Downloads\ATTENDEASE\ATTENDEASE\logo.png'
print(f"Resolved path: {logo_path}")

# Check if the logo exists
if os.path.exists(logo_path):
    try:
        original_logo = Image.open(logo_path)
        resized_logo = original_logo.resize((150, 80), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(resized_logo)
        logo_label = tk.Label(header, image=logo, bg="white")
        logo_label.pack(side="left", padx=20)
    except Exception as e:
        print(f"Error loading logo: {e}")
        logo_label = tk.Label(header, text="Logo Missing", bg="white", fg="red", font=("Arial", 12, "bold"))
        logo_label.pack(side="left", padx=20)
else:
    print(f"Logo not found at {logo_path}")
    logo_label = tk.Label(header, text="Logo Missing", bg="white", fg="red", font=("Arial", 12, "bold"))
    logo_label.pack(side="left", padx=20)

# Welcome message
welcome_message = tk.Label(
    root,
    text="Welcome to AttendEase Portal",
    font=("Arial", 22, "bold"),
    bg="#f0f8ff",
    fg="black"
)
welcome_message.pack(pady=20)

# Button container
button_container = tk.Frame(root, bg="#f0f8ff")
button_container.pack(pady=50)

# Student button
student_button = tk.Button(
    button_container,
    text="Student",
    font=("Arial", 16, "bold"),
    bg="purple",
    fg="white",
    padx=25,
    pady=10,
    relief="raised",
    bd=3,
    command=open_student
)
student_button.grid(row=0, column=1, padx=20)

# Admin button
admin_button = tk.Button(
    button_container,
    text="Admin",
    font=("Arial", 16, "bold"),
    bg="purple",
    fg="white",
    padx=25,
    pady=10,
    relief="raised",
    bd=3,
    command=open_admin
)
admin_button.grid(row=0, column=0, padx=20)

# Footer
footer = tk.Frame(root, bg="white", height=50)
footer.pack(fill="x", side="bottom")

footer_label = tk.Label(
    footer,
    text="AttendEase © 2024 | All rights reserved",
    font=("Arial", 10),
    bg="white",
    fg="gray"
)

footer_label.pack(pady=10)

# Run the application
root.mainloop()
