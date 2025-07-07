import datetime
import time
import tkinter as tk
from tkinter import messagebox
import os
import platform

# Detect host path based on OS
if platform.system() == "Windows":
    host_path = r"C:\Windows\System32\drivers\etc\hosts"
else:
    host_path = "/etc/hosts"

redirect = "127.0.0.1"
site_block = []
log_file = "block_log.txt"

# Function to log block session
def log_session(websites, duration_minutes):
    with open(log_file, "a") as log:
        log.write(f"[{datetime.datetime.now()}] Blocked: {websites} for {duration_minutes} minutes\n")

# Function to block websites
def block_sites(websites, end_time):
    while datetime.datetime.now() < end_time:
        with open(host_path, "r+") as file:
            content = file.read()
            for site in websites:
                if site not in content:
                    file.write(f"{redirect} {site}\n")
        time.sleep(5)

    # Unblock after time ends
    with open(host_path, "r+") as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not any(site in line for site in websites):
                file.write(line)
        file.truncate()

# Function on GUI button press
def start_blocking():
    websites = entry_sites.get().split(",")
    try:
        duration = int(entry_time.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for time.")
        return

    end_time = datetime.datetime.now() + datetime.timedelta(minutes=duration)
    log_session(websites, duration)
    messagebox.showinfo("Blocking Started", f"Blocking {websites} for {duration} minutes")
    window.destroy()
    block_sites(websites, end_time)

# GUI Setup
window = tk.Tk()
window.title("Website Blocker")
window.geometry("400x250")

tk.Label(window, text="Enter websites to block (comma-separated):").pack(pady=10)
entry_sites = tk.Entry(window, width=50)
entry_sites.insert(0, "www.youtube.com, www.facebook.com")
entry_sites.pack()

tk.Label(window, text="Block duration (minutes):").pack(pady=10)
entry_time = tk.Entry(window, width=20)
entry_time.insert(0, "60")
entry_time.pack()

tk.Button(window, text="Start Blocking", command=start_blocking, bg="red", fg="white").pack(pady=20)

tk.Label(window, text="Made with ❤️ by Naveen", font=("Arial", 11)).pack(side="bottom", pady=5)

window.mainloop()
