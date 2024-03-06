# -*- coding: utf-8 -*-
import subprocess
import logging
from win10toast import ToastNotifier
import tkinter as tk

# Initialize logging
logging.basicConfig(filename='network_monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to send desktop alert
def send_desktop_alert(message):
    # For Windows, you can display a message box instead
    try:
        toaster = ToastNotifier()
        toaster.show_toast("Network Alert", message, duration=10)
    except Exception as e:
        print(f"Error occurred while displaying desktop alert: {e}")

# Function to log status
def log_status(status):
    logging.info(status)

# Function to ping a host
def ping_host(host):
    result = subprocess.run(['ping', '-n', '4', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

# List of company branch IP addresses
branch_ips = {
    'Printer': '192.168.1.125'
}
# Main monitoring function
def monitor_network():
    status_window = tk.Tk()
    status_window.title("Network Status")

    for i, (branch, ip) in enumerate(branch_ips.items()):
        status_label = tk.Label(status_window, text=f"{branch} - {ip} ....... ")
        status_label.grid(row=i, column=0)

        if not ping_host(ip):
            message = f"Network down at {branch} ({ip})"
            send_desktop_alert(message)
            status_label.config(text=f"{branch} - {ip} ... DOWN")
        else:
            message = f"Network up at {branch} ({ip})"
            log_status(message)
            status_label.config(text=f"{branch} - {ip} ... OK")

    status_window.mainloop()

# Run the monitoring function
monitor_network()
