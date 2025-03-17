Features
Ping Monitoring: Checks connectivity to a list of IP addresses.
Email Notifications: Sends email alerts for successful and failed pings.
Logging: Logs actions and errors for troubleshooting.
Requirements
Python 3.x
Internet access for email sending
Dependencies
This script uses the following Python libraries:

smtplib
email (email.mime.multipart, email.mime.text)
subprocess
logging
Installation
Clone the repository:
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
Set Up Python Environment:
It's recommended to use a virtual environment.
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies:
This script uses standard libraries, but if you need any additional libraries, install them using:
pip install -r requirements.txt
Configuration
Email Credentials:
Update the send_email function to use a secure method for handling the email credentials (e.g., environment variables).
IP Addresses:
Update the ip_addresses dictionary in the script to include all IPs you wish to monitor along with their descriptive tags.
Email Recipients:
Define email addresses for success_emails, failure_emails, and consolidated_emails to receive ping results.
Usage
To run the script, execute:

python network_ping_monitor.py
Customization
Platform Compatibility
The current script uses Windows-specific ping flags. For Unix-like systems, replace -n with -c in the ping_ip function.
Email Security
Consider using environmental variables or a secure vault for handling email credentials.
External Configuration
To improve usability, configure IP lists and email recipients outside the script, such as in a configuration file (e.g., JSON, YAML).
Logging
Log files are generated with the name email_log.log in the script directory for debugging purposes.
Contributing
Contributions are welcome! Please create an issue or submit a pull request with any improvements or bug fixes.
