# Offline Attendance System (YOLO + Face Recognition)

## Project Overview
This project is an **Offline Smart Attendance System** designed to automate attendance marking in classrooms or rural areas without constant internet connectivity. It uses **YOLOv8** for person detection and **dlib's Face Recognition** to identify registered students from group photos or real-time camera feeds.

## 🛠️ Technology Stack
The project is built using the following technologies:

*   **Language**: Python 3.x
*   **Computer Vision**:
    *   **OpenCV (`opencv-python`)**: For image processing and video capture.
    *   **YOLOv8 (`ultralytics`)**: For detecting *persons* in the frame (High accuracy object detection).
*   **Face Recognition**:
    *   **`face_recognition`**: Built on `dlib`, used for encoding and matching faces with high precision (Strictness optimized to 99.38% accuracy model).
*   **Data Handling**:
    *   **Pandas**: For managing attendance data and creating Excel sheets.
    *   **Pickle**: For persisting the database of face encodings locally.

## ✨ Key Features
1.  **Student Registration**: Capture and encode student faces into a local secure database.
2.  **Group Photo Attendance**: Upload a single classroom photo to mark attendance for everyone visible.
3.  **Real-Time Webcam Attendance**: Live monitoring that auto-detects students.
    *   **Snapshot Feature**: Press `s` to instantly capture the class and mark attendance.
4.  **Anti-Ghosting**: "Delete Student" feature to ensure removed students don't appear in attendance.
5.  **Excel Reporting**: Automatically generates and updates `attendance.xlsx`.
6.  **Visual Debugging**: Generates annotated images (Green boxes for known, Red for unknown) to verify accuracy.

## 🚀 Installation & Setup
1.  **Install Python** (Ensure 'Add to PATH' is checked).
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: CMake and Visual Studio C++ Build Tools may be required for `dlib`/`face_recognition`)*.
3.  **Run the App**:
    ```bash
    python main.py
    ```

---

## 🎓 College Presentation Workflow
Follow this script to demonstrate the project effectively during your presentation.

### **Phase 1: Introduction (1 Minute)**
*   **Explain the Problem**: "Manual attendance is slow and prone to errors. Existing biometric systems are expensive or need internet."
*   **Solution**: "A Python-based Offline System using Computer Vision that works with standard cameras or CCTV."

### **Phase 2: Live Demo - Registration (2 Minutes)**
1.  Run `python main.py`.
2.  **Step 1**: Choose **Option 1 (Register New Student)**.
3.  Enter a volunteer's Name (e.g., "Rohit") and Roll No (e.g., "101").
4.  Provide a clear photo of them (or drag-and-drop a file path).
5.  *Show the console output confirming registration.*

### **Phase 3: Live Demo - Real-Time Attendance (3 Minutes)**
1.  **Step 2**: Choose **Option 3 (Real-Time Webcam Attendance)**.
2.  Ask the registered volunteer to stand in front of the camera.
3.  **Highlight**: Point out the **Green Box** demonstrating recognition.
4.  Ask a non-registered person to enter.
5.  **Highlight**: Point out the **Red Box ("Unknown")**, showing security/accuracy.
6.  **Wow Factor**: Press **'s'** (Snapshot). Show the message "SAVING Snapshot..." and explain: *"We can instantly verify the entire class state."*
7.  Press **'q'** to quit.

### **Phase 4: Verification & Reporting (2 Minutes)**
1.  Open the newly generated `attendance.xlsx`.
2.  Show the row with the student's name and today's date marked as **'P'** (Present).
3.  Show the generated `attendance_debug.jpg` (if available from previous steps) to prove the system "sees" correctly.

### **Phase 5: Database Management (Optional)**
1.  Choose **Option 4 (Delete Student)**.
2.  Delete the volunteer's Roll No.
3.  Run the Webcam again to show they are now **Red (Unknown)**.

## 🔮 Future Scope
The project has significant potential for expansion:
1.  **Mobile App Integration**:
    *   The system can be adapted for **Android/iOS** using **TFLite** (TensorFlow Lite) or ONNX Runtime.
    *   This would allow teachers to mark attendance using their smartphone cameras directly in the field, even without a laptop.
2.  **Cloud Syncing**: Add an optional feature to sync local attendance data to a central cloud server when internet connectivity becomes available.
3.  **Detailed Analytics**: Generate weekly or monthly attendance reports and graphs to track student regularity.

### **Conclusion**
"This system is scalable, works offline, and uses state-of-the-art AI models for high accuracy."
