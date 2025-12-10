import sys
import os
from src.registration import register_student
from src.attendance import process_group_photo, process_webcam
from src.database import delete_student_by_roll

def main():
    print("====================================")
    print("   Offline Attendance System (YOLO)")
    print("====================================")
    
    while True:
        print("\nMenu:")
        print("1. Register New Student")
        print("2. Mark Attendance (Process Group Photo)")
        print("3. Real-Time Webcam Attendance")
        print("4. Delete Student")
        print("5. Exit")
        
        choice = input("Enter simple choice (1-5): ").strip()
        
        if choice == '1':
            print("\n--- Register Student ---")
            name = input("Enter Student Name: ").strip()
            roll_no = input("Enter Roll No: ").strip()
            if not name or not roll_no:
                print("Error: Name and Roll No are required.")
                continue
                
            image_path = input("Enter path to student's photo: ").strip()
            image_path = image_path.replace('"', '').replace("'", "")
            
            if not os.path.exists(image_path):
                print("Error: File not found.")
                continue
                
            try:
                register_student(name, roll_no, image_path)
            except Exception as e:
                print(f"An error occurred: {e}")
                
        elif choice == '2':
            print("\n--- Mark Attendance ---")
            image_path = input("Enter path to Group Photo: ").strip()
            image_path = image_path.replace('"', '').replace("'", "")
            
            if not os.path.exists(image_path):
                print("Error: File not found.")
                continue
                
            try:
                process_group_photo(image_path)
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '3':
            print("\n--- Real-Time Attendance ---")
            try:
                source = 0
                val = input("Enter Camera Index (default 0) or RTSP URL (Press Enter for 0): ").strip()
                if val:
                    if val.isdigit():
                        source = int(val)
                    else:
                        source = val
                process_webcam(source)
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '4':
            print("\n--- Delete Student ---")
            roll_no = input("Enter Roll No to delete: ").strip()
            if not roll_no:
                print("Error: Roll No is required.")
                continue
            
            try:
                delete_student_by_roll(roll_no)
            except Exception as e:
                print(f"An error occurred: {e}")
                
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
