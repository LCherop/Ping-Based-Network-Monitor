# -*- coding: utf-8 -*-
import asyncio
import subprocess
import logging
from win10toast import ToastNotifier
import tkinter as tk
import time
import re

# Initialize logging
logging.basicConfig(filename='network_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to send desktop alert
def send_desktop_alert(message):
    try:
        toaster = ToastNotifier()
        toaster.show_toast("Network Alert", message, duration=10)
    except Exception as e:
        print(f"Error occurred while displaying desktop alert: {e}")

# Function to log status
def log_status(status):
    logging.info(status)


#Function to ping a host
async def ping_host(host,max_retries=4,retry_delay=1):
    for _ in range(max_retries + 1):
        process = await asyncio.create_subprocess_exec(
            'ping', '-n', '4', host, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        await process.communicate()
        if process.returncode == 0:
            return True
        else:
            await asyncio.sleep(retry_delay)
    return False
    

# List of company branch IP addresses
branch_ips = {
    'Branch1':'x.x.x.x',
    'Branch2':'x.x.x.x',
}

#Check for valid IPs
def is_valid_ip(ip):
    # Regular expression pattern for IPv4 address
    ipv4_pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'

    # Check if the IP matches the pattern
    match = re.match(ipv4_pattern, ip)
    
    if match:
        # Check if each octet is between 0 and 255
        for octet in match.groups():
            if not (0 <= int(octet) <= 255):
                return False
        return True
    else:
        return False

# Main monitoring function
async def monitor_network():
    # Setup window
    status_window = tk.Tk()
    status_window.title("Network Status")
    
    # Set the window size
    window_width = 400
    window_height = 250
    status_window.geometry(f"{window_width}x{window_height}")
    
    # Get the screen width and height
    screen_width = status_window.winfo_screenwidth()
    screen_height = status_window.winfo_screenheight()
    
    # Calculate the position to place the window at the bottom right corner
    x_position = screen_width - window_width
    y_position = screen_height - window_height
    
    # Set the window position
    status_window.geometry(f"+{x_position}+{y_position}")

    # Create a frame for the labels
    frame = tk.Frame(status_window, bg="#f0f0f0")  # Light gray background
    frame.pack(fill=tk.BOTH, expand=True)
    
    async def ping_and_update_status(branch, ip, status_label,max_timeout=10):
        start_time = time.time()
        while True:
            if not await ping_host(ip):
                elapsed_time = time.time() - start_time  
                if elapsed_time >= max_timeout:
                    message = f"Network down at {branch} ({ip})"
                    send_desktop_alert(message)
                    log_status(message)
                    status_label.config(text=f"{branch} - {ip} ... DOWN", fg="red")
                    break
                else:
                    message = f"Network down at {branch} ({ip})"
                    #send_desktop_alert(message)
                    log_status(message)
                    status_label.config(text=f"{branch} - {ip} ... DOWN", fg="red")
                    break
            else:
                message = f"Network up at {branch} ({ip})"
                log_status(message)
                status_label.config(text=f"{branch} - {ip} ... OK", fg="green")
                break        
    # Create tasks for pinging each IP address
    tasks = []
    for i, (branch, ip) in enumerate(branch_ips.items()):
        if is_valid_ip(ip):
            status_label = tk.Label(frame, text=f"{branch} - {ip} ....... ", bg="#f0f0f0", fg="black", font=("Arial", 9))
            status_label.pack(fill=tk.X, padx=10, pady=5)
            task = ping_and_update_status(branch, ip, status_label)
            tasks.append(task)
        else:
            print(f"Skipping invalid IP address for {branch}: {ip}")

    # Wait for all tasks to complete
    await asyncio.gather(*tasks)

    status_window.mainloop()

# Run the monitoring function
asyncio.run(monitor_network())
