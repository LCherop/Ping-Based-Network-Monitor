# Ping-Based-Network-Monitor

Ping-Based-Network-Health-Monitor is a program designed to monitor network health based on ping responses. It provides real-time monitoring of servers or network devices, allowing you to quickly identify any issues or downtime.

### Requirements:
- Python needs to be installed on the device.

### Installation:
After installing Python, you'll need to install `win10toast` or `plyer` for desktop toast notifications. You can install it via pip by running the following command in the command prompt:

```bash
pip install win10toast
```
OR 

```bash
pip install win10toast
```

### Usage:
1. Add your server IPs in the branch IP section of the script along with their names, like so:
   ```python
   branch_ips = {
       'Branch1': '192.168...',
       'Branch2': '192.168...',
       # Add more branches as needed
   }
   ```

2. Run the script from the command prompt:
   ```bash
   python pnhmonitor.py
   ```

### Logging:
- When the script is run, it creates a `network_monitor.log` file in the same directory, which logs network health. Each log entry includes a timestamp, status (up/down), and the name/IP of the branch/server.

Example log entries:
```
2024-03-06 16:33:42,721 - INFO - Network up at 8.8.8.8
2024-03-06 16:34:16,551 - INFO - Network up at 8.8.8.8
2024-03-06 16:41:10,819 - INFO - Network up at Google (8.8.8.8)
2024-03-06 16:41:35,107 - INFO - Network up at Google (8.8.8.8)
```

### Note:
- This program is designed to run on Windows devices.
- The `win10toast` library is required for desktop toast notifications.
- Ensure that Python is installed and added to the system PATH for the script to run smoothly.

Enjoy monitoring your network health with Ping-Based-Network-Health-Monitor!
