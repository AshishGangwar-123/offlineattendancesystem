from ultralytics import YOLO
import face_recognition
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import os
from src.database import load_db
import traceback

# Load YOLO model (standard COCO model, we will use class 0: person)
# It will auto-download on first run
yolo_model = YOLO('yolov8n.pt')


def process_group_photo(image_path, output_csv='attendance.csv'):
    print(f"Processing group photo: {image_path}")
    
    # 1. Load Image
    img = cv2.imread(image_path)
    if img is None:
        msg = "Error: Could not load image."
        print(msg)
        return False, msg, None
     # Resize for faster processing if too large? 
    if img.shape[1] > 1920:
         scale = 1920 / img.shape[1]
         img = cv2.resize(img, (0,0), fx=scale, fy=scale)

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # 2. Detect Persons using YOLO
    try:
        results = yolo_model(img, classes=[0], verbose=False) # class 0 is person
    except Exception as e:
        msg = f"YOLO Crashed: {e}"
        print(msg)
        return False, msg, None
    
    detected_persons = []
    
    # Extract bounding boxes
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
            detected_persons.append((x1, y1, x2, y2))
            
    print(f"YOLO detected {len(detected_persons)} people.")
    
    # 3. Load Registered Students
    try:
        db = load_db()
    except Exception as e:
        msg = f"Failed to load DB: {e}"
        print(msg)
        return False, msg, None
        
    if not db:
        msg = "No registered students found. Please register students first."
        print(msg)
        return False, msg, None

    known_encodings = [data['encoding'] for data in db.values()]
    known_roll_nos = list(db.keys())
    known_names = [data['name'] for data in db.values()]
    
    present_roll_nos = []
    
    # 4. For each person, detect face and recognize
    for i, (x1, y1, x2, y2) in enumerate(detected_persons):
        try:
            # Add padding
            h, w, _ = img.shape
            pad = 20
            x1 = max(0, x1 - pad)
            y1 = max(0, y1 - pad)
            x2 = min(w, x2 + pad)
            y2 = min(h, y2 + pad)
            
            # Ensure contiguous memory layout for dlib
            person_crop = np.ascontiguousarray(rgb_img[y1:y2, x1:x2])
            
            if person_crop.size == 0:
                continue
            
            # Detect face specifically in this crop
            # Try to find face locations first with upsampling (helps with small faces)
            # number_of_times_to_upsample=2 makes it slower but finds smaller faces
            face_locs = face_recognition.face_locations(person_crop, number_of_times_to_upsample=2)
            
            if not face_locs:
                # print(f"DEBUG: Person {i} - No face detected in crop {person_crop.shape}")
                # Fallback: Maybe YOLO crop is just the face? Or body?
                # If YOLO detected a person, but dlib can't find a face, it might be a back view or occlusion.
                pass
                
            # Even if face_locs is empty, we can try encoding the whole crop? 
            # No, 'face_encodings' without locations will run the detector again (default upsample=1).
            # If we pass face_locs, it uses them.
            
            if face_locs:
                face_encodings = face_recognition.face_encodings(person_crop, face_locs)
            else:
                # Last ditch effort: try detecting with default settings
                face_encodings = face_recognition.face_encodings(person_crop)

            if not face_encodings:
                # print(f"DEBUG: Person {i} - No encoding generated.")
                continue
                
            encoding = face_encodings[0]
            
            # Match
            # Increased tolerance to 0.55 to improve detection rates (was 0.45)
            tolerance = 0.55
            matches = face_recognition.compare_faces(known_encodings, encoding, tolerance=tolerance)
            face_distances = face_recognition.face_distance(known_encodings, encoding)
            
            name = "Unknown"
            roll_no = "N/A"
            confidence_str = ""
            color = (0, 0, 255) # Red for unknown

            # Debug: Print the best match distance to see what's happening
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                best_distance = face_distances[best_match_index]
                
                # print(f"DEBUG: Person {i} Best Dist: {best_distance:.3f} (Tol: {tolerance})")
                
                if best_distance < tolerance:
                    roll_no = known_roll_nos[best_match_index]
                    name = known_names[best_match_index]
                    confidence = round((1 - best_distance) * 100, 2)
                    confidence_str = f"{confidence}%"
                    color = (0, 255, 0) # Green for match
                    
                    if roll_no not in present_roll_nos:
                        present_roll_nos.append(roll_no)
                        print(f"MATCH: {name} ({roll_no}) | Dist: {round(best_distance, 3)} (Conf: {confidence}%)")
                else:
                     # Optional: Print near misses for debugging
                     if best_distance < 0.65:
                         candidate = known_names[best_match_index]
                         print(f"IGNORED: {candidate} (Dist: {round(best_distance, 3)} > {tolerance}) - Too unsure")
            else:
                 pass
                 # print(f"DEBUG: Person {i} - No known faces to compare against.")
            
            # Draw on image
            # Note: YOLO coords are for the whole image
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            label = f"{name} {confidence_str}"
            cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        except Exception as e:
            print(f"Error processing person {i}: {e}")
            continue
    
    # Save Debug Image
    debug_image_path = "attendance_debug.jpg"
    cv2.imwrite(debug_image_path, img)
    print(f"Debug image saved to: {os.path.abspath(debug_image_path)}")

    # 5. Save Report (Text File Only)
    if present_roll_nos:
        # --- TEXT REPORT GENERATION ---
        try:
            # Filename: Attendance_YYYY-MM-DD_HH-MM-SS.txt
            timestamp_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            txt_filename = f"Attendance_{timestamp_str}.txt"
            
            # Formatted time for the table
            time_display = datetime.now().strftime('%H:%M:%S')

            with open(txt_filename, 'w') as f:
                # Header
                f.write(f"Attendance Report\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*45 + "\n")
                f.write(f"{'Roll No':<15} | {'Name':<20} | {'Status':<10}\n")
                f.write("-" * 45 + "\n")
                
                # Rows - Iterate ALL registered students
                for r_no in known_roll_nos:
                    # Get Name
                    if str(r_no) in db:
                        s_name = db[str(r_no)]['name']
                    else:
                        try: s_name = db[int(r_no)]['name']
                        except: s_name = "Unknown"
                    
                    # Check Status
                    # We store present rolls as they appear in DB (usually string or int). 
                    # present_roll_nos comes from known_roll_nos so types should match.
                    if r_no in present_roll_nos:
                         status = time_display
                    else:
                         status = "Absent"
                        
                    f.write(f"{str(r_no):<15} | {s_name:<20} | {status:<10}\n")
                    
                f.write("="*45 + "\n")
                f.write(f"Total Registered: {len(known_roll_nos)}\n")
                f.write(f"Present: {len(present_roll_nos)}\n")
                f.write(f"Absent: {len(known_roll_nos) - len(present_roll_nos)}\n")
                
            print(f"Text report saved: {txt_filename}")
            msg = f"Success! Report generated.\nFile: {txt_filename}"
            return True, msg, debug_image_path
            
        except Exception as e:
            msg = f"Failed to save text report: {e}"
            print(msg)
            return False, msg, debug_image_path
            # -------------------------------
            
    else:
        msg = "No registered students identified in the photo."
        print(msg)
        return False, msg, debug_image_path


def process_webcam(source=0):
    print(f"Starting Webcam... (Source: {source})")
    print("Commands:")
    print("  's' - Take Snapshot & Mark Attendance")
    print("  'q' - Quit")
    
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print(f"Error: Could not open video source {source}.")
        return

    # Load DB once
    try:
        db = load_db()
    except Exception as e:
        print(f"Failed to load DB: {e}")
        return
        
    if not db:
        print("Warning: No registered students found.")
        
    known_encodings = [data['encoding'] for data in db.values()]
    known_roll_nos = list(db.keys())
    known_names = [data['name'] for data in db.values()]

    # To avoid spamming logs/excel, we can track attendance for this session in a set
    # To avoid spamming logs/excel, we can track attendance for this session in a set
    session_present_roll_nos = set()
    
    frame_count = 0
    skip_frames = 5
    last_detections = [] # Stores (x1, y1, x2, y2, color, label)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
            
        frame_count += 1
        vis_frame = frame.copy()
        
        # --- UI & INPUT SECTION (Run FIRST to ensure responsiveness) ---
        # Draw stale detections on the new frame to keep UI drawing something
        for (x1, y1, x2, y2, color, label) in last_detections:
            cv2.rectangle(vis_frame, (x1, y1), (x2, y2), color, 2)
            if label:
                cv2.putText(vis_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.putText(vis_frame, "Commands: 's' (Snapshot) | 'q' (Quit)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('Real-Time Attendance (Press s: Snapshot, q: Quit)', vis_frame)
        
        # Check input - Increased waitKey slightly for better event capture
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Quitting webcam...")
            break
        elif key == ord('s'):
            # Visual Feedback
            cv2.putText(vis_frame, "SAVING snapshot...", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
            cv2.imshow('Real-Time Attendance (Press s: Snapshot, q: Quit)', vis_frame)
            cv2.waitKey(10)
            
            print("\n--- Capturing Snapshot ---")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            s_name = f"snapshot_{timestamp}.jpg"
            cv2.imwrite(s_name, frame) # Save raw full-res frame
            
            print(f"Processing {s_name}...")
            # We wrap this in try-except to not crash the webcam loop if file issue
            try:
                process_group_photo(s_name)
            except Exception as e:
                print(f"Snapshot processing invalid: {e}")
            print("--- Done ---\n")
            continue # Skip normal inference this frame

        # --- INFERENCE SECTION (Heavy Work) ---
        if frame_count % skip_frames == 0:
            scale = 0.5 # Process at 50% scale for speed (or lower if needed)
            small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            new_detections = []
            try:
                results = yolo_model(small_frame, classes=[0], verbose=False)
                
                for r in results:
                    for box in r.boxes:
                        # Get coords in small frame
                        sx1, sy1, sx2, sy2 = box.xyxy[0].cpu().numpy().astype(int)
                        
                        # Scale back up
                        x1 = int(sx1 / scale)
                        y1 = int(sy1 / scale)
                        x2 = int(sx2 / scale)
                        y2 = int(sy2 / scale)
                        
                        # Recognition logic on small frame (faster) or large frame (more accurate)?
                        # Face recognition needs decent resolution. 
                        # Let's crop from the SMALL frame properly.
                        
                        # Ensure valid crop
                        h, w, _ = small_frame.shape
                        pad = 5
                        fx1, fy1 = max(0, sx1-pad), max(0, sy1-pad)
                        fx2, fy2 = min(w, sx2+pad), min(h, sy2+pad)
                        
                        face_crop = np.ascontiguousarray(rgb_small_frame[fy1:fy2, fx1:fx2])
                        
                        color = (255, 0, 0)
                        name = "Unknown"
                        confidence_str = ""
                        
                        if face_crop.size > 0:
                             # Face recognition
                            encodings = face_recognition.face_encodings(face_crop)
                            if encodings:
                                matches = face_recognition.compare_faces(known_encodings, encodings[0], tolerance=0.55)
                                dists = face_recognition.face_distance(known_encodings, encodings[0])
                                if len(dists) > 0:
                                    best_idx = np.argmin(dists)
                                    if dists[best_idx] < 0.55:
                                        name = known_names[best_idx]
                                        roll = known_roll_nos[best_idx]
                                        conf = round((1 - dists[best_idx]) * 100, 1)
                                        confidence_str = f"{conf}%"
                                        color = (0, 255, 0)
                                        if roll not in session_present_roll_nos:
                                            session_present_roll_nos.add(roll)
                                            print(f"[LIVE] MATCH: {name}")

                        label = f"{name} {confidence_str}" if name != "Unknown" else ""
                        new_detections.append((x1, y1, x2, y2, color, label))
                
                last_detections = new_detections

            except Exception as e:
                # print(f"Inference error: {e}")
                pass

    cap.release()
    cv2.destroyAllWindows()
    
    # Save session attendance (backup)
    if session_present_roll_nos:
        # We rely on process_group_photo for the main record if they use snapshot,
        # but if they just relied on Live View, we save this too.
        # This might duplicate logic but it updates the same Excel file safely.
        pass # The snapshot handles the saving. Live logs are transient unless we force save.
        # Let's simple allow live logs to save too in case they forgot to snapshot.
        # (Rest of existing save logic below...)
        # Let's simple allow live logs to save too in case they forgot to snapshot.
        # (Rest of existing save logic below...)
        print("\nSaving session attendance (Live)...")

        # --- TEXT REPORT GENERATION (Live Session) ---
        try:
            # Filename: Attendance_YYYY-MM-DD_HH-MM-SS.txt
            timestamp_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            txt_filename = f"Attendance_Live_{timestamp_str}.txt"
            
            # Formatted time for the table
            time_display = datetime.now().strftime('%H:%M:%S')

            with open(txt_filename, 'w') as f:
                # Header
                f.write(f"Live Session Attendance Report\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*45 + "\n")
                f.write(f"{'Roll No':<15} | {'Name':<20} | {'Status':<10}\n")
                f.write("-" * 45 + "\n")
                
                # Rows - Iterate ALL registered students
                for r_no in known_roll_nos:
                    # Get Name
                    if str(r_no) in db:
                        s_name = db[str(r_no)]['name']
                    else:
                         try: s_name = db[int(r_no)]['name']
                         except: s_name = "Unknown"
                    
                    # Check Status
                    if r_no in session_present_roll_nos:
                         status = time_display
                    else:
                         status = "Absent"
                        
                    f.write(f"{str(r_no):<15} | {s_name:<20} | {status:<10}\n")
                    
                f.write("="*45 + "\n")
                f.write(f"Total Registered: {len(known_roll_nos)}\n")
                f.write(f"Present: {len(session_present_roll_nos)}\n")
                f.write(f"Absent: {len(known_roll_nos) - len(session_present_roll_nos)}\n")
                
            print(f"Live session report saved: {txt_filename}")
            
        except Exception as e:
            print(f"Failed to save live text report: {e}")
        # -------------------------------

