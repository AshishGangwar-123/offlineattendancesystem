import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import sys

# Add the project root to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class OfflineAttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Offline Attendance System")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        # --- Theme & Colors ---
        self.colors = {
            "bg_dark": "#1e1e2e",       # Main Background
            "sidebar": "#252535",       # Sidebar Background
            "accent": "#7aa2f7",        # Buttons / Highlights
            "text": "#c0caf5",          # Main Text
            "text_light": "#ffffff",    # Light Text
            "success": "#9ece6a",       # Green
            "warning": "#e0af68",       # Yellow
            "danger": "#f7768e",        # Red
            "frame_bg": "#24283b"       # Content Frame Background
        }
        
        self.configure(bg=self.colors["bg_dark"])
        self.setup_style()
        
        # --- Layout ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar_frame = tk.Frame(self, bg=self.colors["sidebar"], width=250)
        self.sidebar_frame.grid(row=0, column=0, sticky="ns")
        self.sidebar_frame.grid_propagate(False)
        
        # Content Area
        self.content_frame = tk.Frame(self, bg=self.colors["bg_dark"])
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # --- Frames ---
        self.frames = {}
        self.current_frame = None
        
        self.create_sidebar()
        self.init_frames()
        self.show_frame("HomeFrame")

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # General Frame
        style.configure("TFrame", background=self.colors["bg_dark"])
        
        # Labels
        style.configure("TLabel", background=self.colors["bg_dark"], foreground=self.colors["text"], font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI", 24, "bold"), foreground=self.colors["text_light"])
        style.configure("SubHeader.TLabel", font=("Segoe UI", 16), foreground=self.colors["accent"])
        
        # Buttons
        style.configure("TButton", 
                        font=("Segoe UI", 11, "bold"), 
                        background=self.colors["accent"], 
                        foreground="white",
                        borderwidth=0,
                        focuscolor=self.colors["bg_dark"])
        style.map("TButton", background=[("active", "#5d87e0")])
        
        style.configure("Danger.TButton", background=self.colors["danger"])
        style.map("Danger.TButton", background=[("active", "#d95e74")])

        # Entry
        style.configure("TEntry", fieldbackground="#2f334d", foreground="white", borderwidth=0, insertcolor="white")
        
    def create_sidebar(self):
        # Title / Brand
        title_label = tk.Label(self.sidebar_frame, text="ATTENDANCE\nSYSTEM", bg=self.colors["sidebar"], fg=self.colors["accent"], font=("Segoe UI", 18, "bold"), justify="center")
        title_label.pack(pady=30)
        
        # Navigation Buttons
        nav_items = [
            ("Home", "HomeFrame"),
            ("Register Student", "RegisterFrame"),
            ("Group Photo", "AttendancePhotoFrame"),
            ("Live Webcam", "AttendanceWebcamFrame"),
            ("Delete Student", "DeleteFrame"),
        ]
        
        for text, frame_name in nav_items:
            btn = tk.Button(self.sidebar_frame, text=text, 
                            bg=self.colors["sidebar"], fg=self.colors["text"],
                            font=("Segoe UI", 12), borderwidth=0, activebackground=self.colors["frame_bg"], activeforeground=self.colors["text_light"],
                            width=20, pady=10, cursor="hand2", anchor="w", padx=20,
                            command=lambda fn=frame_name: self.show_frame(fn))
            btn.pack(fill="x")
            
        # Exit
        exit_btn = tk.Button(self.sidebar_frame, text="Exit", 
                             bg=self.colors["sidebar"], fg=self.colors["danger"],
                             font=("Segoe UI", 12, "bold"), borderwidth=0, activebackground=self.colors["frame_bg"], activeforeground=self.colors["danger"],
                             width=20, pady=10, cursor="hand2", anchor="w", padx=20,
                             command=self.quit)
        exit_btn.pack(side="bottom", fill="x", pady=20)

    def init_frames(self):
        # We will import these classes or define them in this file. 
        # For now, defining them internally to keep it single-file or easy to split later.
        
        for F in (HomeFrame, RegisterFrame, AttendancePhotoFrame, AttendanceWebcamFrame, DeleteFrame):
            page_name = F.__name__
            frame = F(parent=self.content_frame, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        # Optional: Trigger an 'on_show' event if the frame requires refresh
        if hasattr(frame, "on_show"):
            frame.on_show()

# --- Placeholder Frames ---
class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.colors["bg_dark"])
        self.controller = controller
        
        # Content
        header = ttk.Label(self, text="Welcome Back!", style="Header.TLabel")
        header.pack(pady=(40, 10))
        
        desc = ttk.Label(self, text="Select an option from the sidebar to get started.", font=("Segoe UI", 12))
        desc.pack(pady=5)
        
        # Stats Container (Placeholder)
        stats_frame = tk.Frame(self, bg=controller.colors["frame_bg"], padx=20, pady=20)
        stats_frame.pack(pady=40, fill="x", padx=40)
        
        stat_lbl = tk.Label(stats_frame, text="System Status: Ready", bg=controller.colors["frame_bg"], fg=controller.colors["success"], font=("Segoe UI", 14))
        stat_lbl.pack()


from src.registration import register_student

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.colors["bg_dark"])
        self.controller = controller
        
        # Header
        ttk.Label(self, text="Register New Student", style="Header.TLabel").pack(pady=(30, 20))
        
        # Form Container
        form_frame = tk.Frame(self, bg=controller.colors["bg_dark"])
        form_frame.pack(pady=10)
        
        # Name
        ttk.Label(form_frame, text="Full Name", style="SubHeader.TLabel", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(form_frame, width=30, font=("Segoe UI", 12))
        self.name_entry.grid(row=1, column=0, pady=(0, 15), ipady=5)
        
        # Roll No
        ttk.Label(form_frame, text="Roll Number", style="SubHeader.TLabel", font=("Segoe UI", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.roll_entry = ttk.Entry(form_frame, width=30, font=("Segoe UI", 12))
        self.roll_entry.grid(row=3, column=0, pady=(0, 15), ipady=5)
        
        # Photo Selection
        ttk.Label(form_frame, text="Student Photo", style="SubHeader.TLabel", font=("Segoe UI", 12)).grid(row=4, column=0, sticky="w", pady=5)
        
        photo_box = tk.Frame(form_frame, bg=controller.colors["bg_dark"])
        photo_box.grid(row=5, column=0, sticky="w")
        
        self.photo_path_var = tk.StringVar()
        self.photo_entry = ttk.Entry(photo_box, textvariable=self.photo_path_var, width=22, font=("Segoe UI", 10), state="readonly")
        self.photo_entry.pack(side="left", ipady=5)
        
        btn_browse = ttk.Button(photo_box, text="Browse", width=8, command=self.browse_photo)
        btn_browse.pack(side="left", padx=5)
        
        # Register Button
        register_btn = ttk.Button(self, text="Register Student", width=20, command=self.register_action)
        register_btn.pack(pady=40, ipady=5)
        
        # Status Label
        self.status_label = tk.Label(self, text="", bg=controller.colors["bg_dark"], font=("Segoe UI", 10))
        self.status_label.pack()

    def browse_photo(self):
        filename = filedialog.askopenfilename(title="Select Student Photo", 
                                              filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if filename:
            self.photo_path_var.set(filename)

    def register_action(self):
        name = self.name_entry.get().strip()
        roll = self.roll_entry.get().strip()
        path = self.photo_path_var.get().strip()
        
        if not name or not roll or not path:
            messagebox.showwarning("Incomplete Data", "Please fill in all fields and select a photo.")
            return
            
        # Update UI state
        self.status_label.config(text="Processing...", fg=self.controller.colors["warning"])
        self.update_idletasks()
        
        success, msg = register_student(name, roll, path)
        
        if success:
            messagebox.showinfo("Success", msg)
            self.status_label.config(text="Registration Successful!", fg=self.controller.colors["success"])
            # Clear fields
            self.name_entry.delete(0, tk.END)
            self.roll_entry.delete(0, tk.END)
            self.photo_path_var.set("")
        else:
            messagebox.showerror("Registration Failed", msg)
            self.status_label.config(text="Registration Failed", fg=self.controller.colors["danger"])


from src.attendance import process_group_photo, process_webcam

class AttendancePhotoFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.colors["bg_dark"])
        self.controller = controller
        
        # Header
        ttk.Label(self, text="Mark Attendance (Group Photo)", style="Header.TLabel").pack(pady=(30, 20))
        
        # Input Controls
        ctrl_frame = tk.Frame(self, bg=controller.colors["bg_dark"])
        ctrl_frame.pack(pady=10)
        
        ttk.Label(ctrl_frame, text="Select Group Photo", style="SubHeader.TLabel", font=("Segoe UI", 12)).grid(row=0, column=0, sticky="w", pady=5)
        
        self.photo_path_var = tk.StringVar()
        self.photo_entry = ttk.Entry(ctrl_frame, textvariable=self.photo_path_var, width=40, font=("Segoe UI", 10), state="readonly")
        self.photo_entry.grid(row=1, column=0, ipady=5)
        
        btn_browse = ttk.Button(ctrl_frame, text="Browse", width=10, command=self.browse_photo)
        btn_browse.grid(row=1, column=1, padx=10)
        
        btn_process = ttk.Button(ctrl_frame, text="Process", width=15, command=self.process_photo)
        btn_process.grid(row=2, column=0, columnspan=2, pady=20, ipady=5)
        
        # Result Area
        self.result_label = tk.Label(self, text="Result will appear here", bg="#101015", fg="#555", width=80, height=20)
        self.result_label.pack(pady=10)
        
        # Status Label
        self.status_label = tk.Label(self, text="", bg=controller.colors["bg_dark"], font=("Segoe UI", 10))
        self.status_label.pack()

    def browse_photo(self):
        filename = filedialog.askopenfilename(title="Select Group Photo", 
                                              filetypes=[("Image Files", "*.jpg *.jpeg *.png")])
        if filename:
            self.photo_path_var.set(filename)

    def process_photo(self):
        path = self.photo_path_var.get()
        if not path:
             messagebox.showwarning("No File", "Please select a photo first.")
             return
             
        self.status_label.config(text="Processing... Please Wait", fg=self.controller.colors["warning"])
        self.update_idletasks()
        
        # Process
        success, msg, output_path = process_group_photo(path)
        
        if success:
            self.status_label.config(text=msg.split('\n')[0], fg=self.controller.colors["success"])
            messagebox.showinfo("Attendance Marked", msg)
        else:
            self.status_label.config(text=msg, fg=self.controller.colors["danger"])
            messagebox.showerror("Error", msg)
            
        # Display Image
        if output_path and os.path.exists(output_path):
            self.show_image(output_path)
            
    def show_image(self, path):
        try:
            pil_img = Image.open(path)
            # Resize to fit
            w_box = 600
            h_box = 400
            
            w, h = pil_img.size
            ratio = min(w_box/w, h_box/h)
            
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            
            pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            
            self.tk_img = ImageTk.PhotoImage(pil_img) # Keep ref
            self.result_label.config(image=self.tk_img, text="", width=new_w, height=new_h)
            
        except Exception as e:
            print(f"Error showing image: {e}")
            self.result_label.config(text="Could not display result image.", image="")


import cv2
import numpy as np
from datetime import datetime
from src.database import load_db, delete_student_by_roll

class AttendanceWebcamFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.colors["bg_dark"])
        self.controller = controller
        self.cap = None
        self.is_running = False
        
        # UI Layout
        top_frame = tk.Frame(self, bg=controller.colors["bg_dark"])
        top_frame.pack(side="top", fill="x", padx=20, pady=10)
        
        ttk.Label(top_frame, text="Real-Time Attendance", style="Header.TLabel").pack(side="left")
        
        btn_frame = tk.Frame(top_frame, bg=controller.colors["bg_dark"])
        btn_frame.pack(side="right")
        
        self.btn_start = ttk.Button(btn_frame, text="Start Camera", command=self.start_camera)
        self.btn_start.pack(side="left", padx=5)
        
        self.btn_stop = ttk.Button(btn_frame, text="Stop Camera", command=self.stop_camera, state="disabled")
        self.btn_stop.pack(side="left", padx=5)
        
        self.btn_snap = ttk.Button(btn_frame, text="Snapshot", command=self.take_snapshot, state="disabled")
        self.btn_snap.pack(side="left", padx=5)
        
        # Video Feed
        self.video_label = tk.Label(self, bg="black", text="Camera Off", fg="white")
        self.video_label.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Status
        self.status_label = tk.Label(self, text="Ready", bg=controller.colors["bg_dark"], font=("Segoe UI", 10))
        self.status_label.pack(pady=5)

        # Inference State
        self.db = None
        self.known_encodings = []
        self.known_names = []
        self.known_roll_nos = []
        
        # Check imports for inference
        try:
            from src.attendance import yolo_model
            # face_recognition is imported at top of file usually, but ensure it's here
            import face_recognition
            self.yolo_model = yolo_model
            self.face_recognition = face_recognition
            self.can_run_inference = True
        except ImportError:
            self.can_run_inference = False
            self.status_label.config(text="Warning: Inference libraries not loaded.", fg=controller.colors["danger"])

    def load_resources(self):
        try:
            self.db = load_db()
            if self.db:
                self.known_encodings = [d['encoding'] for d in self.db.values()]
                self.known_names = [d['name'] for d in self.db.values()]
                self.known_roll_nos = list(self.db.keys())
            else:
                self.status_label.config(text="No students registered.", fg=self.controller.colors["warning"])
        except Exception as e:
            print(f"DB Load Error: {e}")

    def start_camera(self):
        if self.is_running: return
        
        self.cap = cv2.VideoCapture(0) # Default camera
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open camera.")
            return
            
        self.is_running = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.btn_snap.config(state="normal")
        
        self.load_resources()
        self.update_frame()
        
    def stop_camera(self):
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.cap = None
        
        self.video_label.config(image="", text="Camera Off")
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.btn_snap.config(state="disabled")
        
    def update_frame(self):
        if not self.is_running or not self.cap:
            return
            
        ret, frame = self.cap.read()
        if ret:
            # Inference (Lightweight version for GUI)
            # We can skip frames or just detect but not recognize every frame to save speed
            # For now, let's just show video. If we want boxes:
            
            # Simple YOLO detection visualization (optional)
            # frame = self.run_inference(frame)
            
            # Convert to RGB for Tkinter
            cv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Resize to fit view if needed
            h, w, _ = cv_img.shape
            # Fixed height 500, maintain aspect
            target_h = 500
            scale = target_h / h
            target_w = int(w * scale)
            
            cv_img = cv2.resize(cv_img, (target_w, target_h))
            
            img = Image.fromarray(cv_img)
            imgtk = ImageTk.PhotoImage(image=img)
            
            self.video_label.imgtk = imgtk # keep ref
            self.video_label.config(image=imgtk, text="")
        
        # Schedule next update
        self.after(10, self.update_frame)

    def take_snapshot(self):
        if not self.cap: return
        ret, frame = self.cap.read()
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            s_name = f"snapshot_{timestamp}.jpg"
            cv2.imwrite(s_name, frame)
            
            # Stop camera to show result? Or just show popup?
            # Let's process it
            success, msg, out_path = process_group_photo(s_name)
            
            if success:
                messagebox.showinfo("Snapshot Processed", msg)
                # Ideally, show the annotated image in a popup or verify tab
            else:
                messagebox.showerror("Processing Failed", msg)

    def on_show(self):
        # Called when frame is shown
        pass
        
    def on_hide(self):
        # Called when switching away
        self.stop_camera()

class DeleteFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.colors["bg_dark"])
        self.controller = controller
        
        ttk.Label(self, text="Delete Student", style="Header.TLabel").pack(pady=40)
        
        form = tk.Frame(self, bg=controller.colors["bg_dark"])
        form.pack()
        
        ttk.Label(form, text="Enter Roll Number to Delete:", style="SubHeader.TLabel").pack(pady=10)
        self.roll_entry = ttk.Entry(form, width=30, font=("Segoe UI", 12))
        self.roll_entry.pack(pady=5, ipady=5)
        
        btn_del = tk.Button(self, text="DELETE STUDENT", 
                            bg=controller.colors["danger"], fg="white",
                            font=("Segoe UI", 11, "bold"),
                            relief="flat",
                            padx=20, pady=10,
                            command=self.delete_action)
        btn_del.pack(pady=30)

    def delete_action(self):
        roll = self.roll_entry.get().strip()
        if not roll:
            messagebox.showwarning("Input Required", "Please enter a roll number.")
            return
            
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student with Roll No: {roll}?\nThis cannot be undone.")
        if confirm:
            try:
                # We need to import delete_student_by_roll or implement it
                # It was imported at top of file? No.
                # Let's import it inside or fix top imports
                success, msg = delete_student_by_roll(roll)
                
                if success:
                    messagebox.showinfo("Success", msg)
                    self.roll_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Deletion Failed", msg)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {e}")



if __name__ == "__main__":
    app = OfflineAttendanceApp()
    app.mainloop()
