import pickle
import os
import pandas as pd

DB_PATH = 'data/db.pkl'

def load_db():
    if not os.path.exists(DB_PATH):
        return {}
    try:
        with open(DB_PATH, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading database: {e}")
        return {}

def save_db(data):
    # Ensure directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    try:
        with open(DB_PATH, 'wb') as f:
            pickle.dump(data, f)
        print("Database saved successfully.")
    except Exception as e:
        print(f"Error saving database: {e}")

def delete_student_by_roll(roll_no):
    db = load_db()
    # Ensure strict string comparison if keys are strings (which they should be)
    if str(roll_no) in db:
        name = db[str(roll_no)]['name']
        del db[str(roll_no)]
        save_db(db)
        msg = f"Successfully deleted student: {name} (Roll No: {roll_no})"
        
        # Also remove from Excel Report if exists
        excel_path = 'attendance.xlsx'
        if os.path.exists(excel_path):
            try:
                df = pd.read_excel(excel_path)
                
                # Robust conversion of Roll No to string, removing .0 if present (common in Pandas read_excel)
                df['Roll No'] = df['Roll No'].apply(lambda x: str(x).split('.')[0] if pd.notnull(x) else "")
                
                target_roll = str(roll_no).split('.')[0]
                
                # Check if roll exists
                if target_roll in df['Roll No'].values:
                    # Filter out
                    df = df[df['Roll No'] != target_roll]
                    try:
                        df.to_excel(excel_path, index=False)
                        msg += "\nRemoved from attendance.xlsx."
                    except PermissionError:
                        msg += "\nERROR: Excel file is OPEN. Close it to update!"
            except Exception as e:
                msg += f"\nWarning: Excel update failed ({e})."
                
        print(msg)
        return True, msg
    else:
        # Check if maybe it's stored as int?
        try:
            if int(roll_no) in db:
                 del db[int(roll_no)]
                 save_db(db)
                 
                 # Also remove from Excel (Int Logic)
                 excel_path = 'attendance.xlsx'
                 removed_excel = False
                 if os.path.exists(excel_path):
                     try:
                         df = pd.read_excel(excel_path)
                         # Robust normalize
                         df['Roll No'] = df['Roll No'].apply(lambda x: str(x).split('.')[0] if pd.notnull(x) else "")
                         target_roll = str(roll_no).split('.')[0]
                         
                         before = len(df)
                         df = df[df['Roll No'] != target_roll]
                         if len(df) < before:
                             df.to_excel(excel_path, index=False)
                             removed_excel = True
                     except: 
                        pass
                 
                 msg = f"Successfully deleted student (Roll No: {roll_no}) [Int Key]"
                 if removed_excel: msg += "\nRemoved from attendance.xlsx."
                 print(msg)
                 return True, msg
        except:
            pass
            
        msg = f"Error: Roll number {roll_no} not found in database."
        print(msg)
        return False, msg
