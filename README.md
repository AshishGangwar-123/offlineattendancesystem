# Offline Smart Attendance System (GUI Version)

## 📌 Project Overview
This project is an **Offline Smart Attendance System** designed to automate attendance marking in classrooms, seminars, or rural areas without internet connectivity. It uses **YOLOv8** for robust person detection and **Face Recognition** (dlib) to identify registered students from group photos or real-time camera feeds. The system features a modern **Tkinter GUI** and generates clear **Text-based Reports** with timestamps.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Language** | **Python 3.x** | Core logic and scripting. |
| **GUI Framework** | **Tkinter** | User Interface (Offline, Lightweight). |
| **Object Detection** | **YOLOv8** (`ultralytics`) | Detecting persons in crowded frames. |
| **Face Recognition** | **`face_recognition`** (dlib) | High-accuracy face encoding & matching. |
| **Image Processing** | **OpenCV** & **Pillow** | Camera feed, resizing, and image manipulation. |
| **Data Storage** | **Pickle** (`.pkl`) | Storing face encodings securely offline. |
| **Reporting** | **Text Files** (`.txt`) | Timestamped, table-formatted attendance logs. |

---

## 🔄 System Flowchart

```mermaid
graph TD
    A[Start Application] --> B{Select Mode}
    
    B -->|Register| C[Enter Name & Roll No]
    C --> D[Upload Student Photo]
    D --> E[Save Face Encoding to DB]
    
    B -->|Group Photo| F[Upload Class Photo]
    F --> G[YOLO: Detect Persons]
    G --> H[Face Rec: Match Encodings]
    H --> I[Generate Attendance Report (.txt)]
    
    B -->|Live Webcam| J[Start Camera Stream]
    J --> K[View Real-Time Feed]
    K -->|Press 'Snapshot'| L[Capture Frame]
    L --> G
    
    B -->|Delete| M[Enter Roll No]
    M --> N[Remove from DB & Logs]
```

---

## 🎯 Applications

1.  **Classrooms & Schools**: Automate daily roll calls instantly using a single group photo.
2.  **Corporate Meetings**: Mark attendance for offline board meetings or training sessions.
3.  **Events & Seminars**: Quick registration and attendance for check-ins at gates.
4.  **Rural Education**: Works perfectly in remote villages with **zero internet** dependency.
5.  **Exams**: Verify student identity before entry.

---

## ✨ Key Features
-   **Modern Dark UI**: Easy-to-use Sidebar navigation.
-   **High Accuracy**: Combines YOLOv8 (to find people) + Upsampled Face Recognition (to identify them).
-   **Anti-Ghosting**: Marks undetected registered students as **"Absent"**.
-   **Timestamped Reports**: Generates a new `.txt` file for every session (e.g., `Attendance_2025-12-11_10-00-00.txt`).
-   **Live Snapshot**: Capture attendance directly from the webcam stream.

---

## 🔮 Future Scope

The project is built to be scalable. Here is the roadmap for future improvements:

1.  **📱 Mobile Application**
    *   Convert the models to **TFLite** or **ONNX**.
    *   Build an Android/iOS app (Flutter/React Native) to allow teachers to take attendance via phone.

2.  **☁️ Cloud Synchronization**
    *   Implement an optional "Sync" button.
    *   When internet is available, upload local `.txt` logs to a central server (Firebase/AWS) for principal review.

3.  **📊 Advanced Analytics Dashboard**
    *   Create a graphical dashboard to visualize attendance trends (e.g., "Attendance vs Time", "Most Absent Students").
    *   Export monthly consolidated reports.

4.  **🔒 Liveness Detection**
    *   Prevent spoofing (using photos of photos) by implementing blink detection or depth analysis.

---

## 🚀 How to Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the GUI**:
    ```bash
    python run_gui.py
    ```
3.  **Use the Sidebar** to Register students, then take Photos/Snapshots to mark attendance!
