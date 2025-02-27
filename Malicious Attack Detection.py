import os
import time
import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime
import threading

# Directory to simulate attack
TARGET_DIR = "test_files"
ENCRYPTED_EXTENSION = ".locked"
DECRYPTION_KEY = "12345"  # Fake key for simulation
LOG_FILE = "history.log"
INITIAL_TIMER = 300  # 5 minutes countdown
timer_running = False
TIMER_DURATION = INITIAL_TIMER

# Ensure target directory exists
if not os.path.exists(TARGET_DIR):
    os.makedirs(TARGET_DIR)
    for i in range(3):  # Create test files
        with open(os.path.join(TARGET_DIR, f"file{i}.txt"), "w") as f:
            f.write("This is a test file.")

def log_action(action):
    """Logs actions with timestamps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {action}\n")
    update_history()

def update_history():
    """Updates the history log display."""
    history_text.config(state=tk.NORMAL)
    history_text.delete(1.0, tk.END)
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as log:
            history_text.insert(tk.END, log.read())
    history_text.config(state=tk.DISABLED)

def update_file_status():
    """Updates the file status display."""
    file_status_text.config(state=tk.NORMAL)
    file_status_text.delete(1.0, tk.END)
    for filename in os.listdir(TARGET_DIR):
        file_status_text.insert(tk.END, filename + "\n")
    file_status_text.config(state=tk.DISABLED)

def encrypt_files():
    """Simulates a ransomware attack by renaming files."""
    global timer_running, TIMER_DURATION
    for filename in os.listdir(TARGET_DIR):
        if not filename.endswith(ENCRYPTED_EXTENSION):
            os.rename(os.path.join(TARGET_DIR, filename), os.path.join(TARGET_DIR, filename + ENCRYPTED_EXTENSION))
    messagebox.showerror("Ransomware Attack!", "Your files have been encrypted! Pay to decrypt.")
    log_action("Files encrypted.")
    update_file_status()
    TIMER_DURATION = INITIAL_TIMER  # Reset timer duration
    timer_running = True  # Start countdown
    start_countdown()

def decrypt_files(event=None):
    """Simulates decryption if the correct key is entered."""
    global timer_running
    key = key_entry.get().strip()
    key_entry.delete(0, tk.END)  # Auto-clear input field

    if key:
        if key == DECRYPTION_KEY:
            for filename in os.listdir(TARGET_DIR):
                if filename.endswith(ENCRYPTED_EXTENSION):
                    os.rename(os.path.join(TARGET_DIR, filename), os.path.join(TARGET_DIR, filename.replace(ENCRYPTED_EXTENSION, "")))
            messagebox.showinfo("Success", "Files decrypted successfully!")
            log_action("Files decrypted.")
            update_file_status()
            timer_running = False  # Stop countdown
            timer_label.config(text="Decryption Successful! Timer Stopped.")
        else:
            messagebox.showerror("Failed", "Wrong decryption key!")
            log_action("Failed decryption attempt.")
    else:
        messagebox.showwarning("Input Required", "Please enter a decryption key.")

def reset_files():
    """Resets files, logs, and the timer for testing."""
    global TIMER_DURATION, timer_running

    # Reset encrypted files
    for filename in os.listdir(TARGET_DIR):
        if filename.endswith(ENCRYPTED_EXTENSION):
            os.rename(os.path.join(TARGET_DIR, filename), os.path.join(TARGET_DIR, filename.replace(ENCRYPTED_EXTENSION, "")))

    # Clear log
    with open(LOG_FILE, "w") as log:
        log.write("")

    # Reset UI elements
    update_history()
    update_file_status()

    # Reset timer
    TIMER_DURATION = INITIAL_TIMER  # Reset to 5 minutes
    timer_label.config(text=f"Time Left: {TIMER_DURATION} sec")
    timer_running = False  # Stop countdown
    messagebox.showinfo("Reset", "Files, logs, and timer have been reset.")
    log_action("System reset.")

def start_countdown():
    """Starts or restarts a ransom countdown timer."""
    global TIMER_DURATION, timer_running

    def countdown():
        global TIMER_DURATION, timer_running
        while TIMER_DURATION > 0 and timer_running:
            time.sleep(1)
            TIMER_DURATION -= 1
            timer_label.config(text=f"Time Left: {TIMER_DURATION} sec")
            if TIMER_DURATION == 0:
                messagebox.showerror("Warning", "Time is up! Files cannot be recovered.")
                log_action("Time expired. Files remain encrypted.")

    threading.Thread(target=countdown, daemon=True).start()

# GUI setup
root = tk.Tk()
root.title("Enhanced Ransomware Simulator")
root.geometry("500x400")
root.configure(bg="#222")

# Header
tk.Label(root, text="Ransomware Simulation", font=("Arial", 13, "bold"), fg="white", bg="#222").pack(pady=10)

# Attack Simulation
encrypt_btn = tk.Button(root, text="Simulate Attack", command=encrypt_files, bg="red", fg="white", font=("Arial", 12))
encrypt_btn.pack(pady=5)

tk.Label(root, text="Enter decryption key:", fg="white", bg="#222").pack(pady=5)
key_entry = tk.Entry(root, width=20, font=("Arial", 12))
key_entry.pack(pady=5)
key_entry.bind("<Return>", decrypt_files)  # Allows pressing Enter to submit key

decrypt_btn = tk.Button(root, text="Decrypt Files", command=decrypt_files, bg="green", fg="white", font=("Arial", 12))
decrypt_btn.pack(pady=5)

reset_btn = tk.Button(root, text="Reset", command=reset_files, bg="blue", fg="white", font=("Arial", 12))
reset_btn.pack(pady=5)

# Timer Label
timer_label = tk.Label(root, text=f"Time Left: {TIMER_DURATION} sec", fg="yellow", bg="#222", font=("Arial", 12))
timer_label.pack(pady=5)

# File Status Display
tk.Label(root, text="File Status:", fg="white", bg="#222").pack(pady=5)
file_status_text = scrolledtext.ScrolledText(root, height=5, width=60, font=("Arial", 10))
file_status_text.pack(pady=5)
file_status_text.config(state=tk.DISABLED)
update_file_status()

# History Log Display
tk.Label(root, text="Action History:", fg="white", bg="#222").pack(pady=5)
history_text = scrolledtext.ScrolledText(root, height=6, width=60, font=("Arial", 10))
history_text.pack(pady=5)
history_text.config(state=tk.DISABLED)

refresh_btn = tk.Button(root, text="Refresh History", command=update_history, bg="gray", fg="white", font=("Arial", 10))
refresh_btn.pack(pady=5)

exit_btn = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12))
exit_btn.pack(pady=10)

update_history()
root.mainloop()
