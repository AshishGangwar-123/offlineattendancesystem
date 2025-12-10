import face_recognition
import cv2
import os
import shutil
from src.database import load_db, save_db

REGISTERED_FACES_DIR = 'data/registered_faces'

def register_student(name, roll_no, image_path):
    print(f"Registering student: {name} ({roll_no}) from {image_path}")
    
    try:
        # Load image
        image = face_recognition.load_image_file(image_path)
        
        # Detect faces
        face_locations = face_recognition.face_locations(image)
        if not face_locations:
            msg = "Error: No face detected in the image."
            print(msg)
            return False, msg
        
        if len(face_locations) > 1:
            msg = "Error: Multiple faces detected. Please provide an image with a single student."
            print(msg)
            return False, msg
            
        # Get encoding
        # we take the first face found
        db = load_db()
        
        # Check if roll_no already exists
        if roll_no in db:
            print(f"Warning: Roll number {roll_no} already exists. Overwriting.")
            
        face_encoding = face_recognition.face_encodings(image, face_locations)[0]
        
        # Save to DB
        db[roll_no] = {
            'name': name,
            'encoding': face_encoding
        }
        save_db(db)
        
        # Save a reference image (optional, but good for UI)
        os.makedirs(REGISTERED_FACES_DIR, exist_ok=True)
        # Convert RGB (face_recognition) to BGR (opencv) for saving
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        target_path = os.path.join(REGISTERED_FACES_DIR, f"{roll_no}_{name}.jpg")
        cv2.imwrite(target_path, image_bgr)
        
        msg = f"Successfully registered {name} ({roll_no})."
        print(msg)
        return True, msg
        
    except Exception as e:
        msg = f"Registration failed: {str(e)}"
        print(msg)
        return False, msg

