Network Monitoring Script
This script is designed to continuously monitor network device availability through ICMP pings. When a device is unreachable, it sends alerts to a specified Google Chat space.

Features
IP Monitoring: Periodically pings a list of IP addresses to verify connectivity.
Alert System: Sends alerts through Google Chat for initial detection of downtime and periodic updates if downtime persists.
Logging: Detailed logging of all events and errors for future review.
Recover Alerts: Notifies when previously downed devices return to normal operation.
Requirements
Python 3.x
Internet access for sending alerts via Google Chat
Dependencies
This script uses the following Python libraries:

subprocess
logging
requests
json
time
datetime
os
concurrent.futures (for threading support)
Install them using:

pip install requests
Note: The other libraries (subprocess, logging, etc.) are part of the Python Standard Library and don't require additional installation.

Setup Instructions
Clone the Repository
[git clone (https://github.com/surya24700-afk/pingmonitoring.git)
cd yourrepository
Configure Logging
Ensure that the LOG_DIR variable points to a valid directory where logs will be saved. The directory should be writable.
IP List Configuration
Modify the ip_addresses dictionary variable within the script to include the IP addresses and associated tags of the devices you wish to monitor.
Set Google Chat Webhook URL
Replace the webhook_url variable in the script with your Google Chat Webhook URL to enable alert messages to be sent to your Google Chat space.
Running the Script
Execute the script using Python:
python network_monitor.py
Alert System
Real-time Alerts: Sent when an IP fails to ping successfully 3 consecutive times.
Periodic Alerts: Sent if the failure condition continues for over an hour beyond initial detection.
Recovery Alerts: Sent when an IP that was previously unreachable is successfully pingable once more.
Logging
Logs are maintained in the directory set by LOG_DIR with separate logs for each day of operation.

Contributing
Contributions are welcomed. Please raise an issue or submit a pull request for any changes or improvements you might have.

License
This project is licensed under the MIT License. See the LICENSE file for details.
