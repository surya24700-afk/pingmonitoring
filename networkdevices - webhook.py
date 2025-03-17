import subprocess
import logging
import requests
import json
import time
import datetime
import os
from concurrent.futures import ThreadPoolExecutor

# Log directory
LOG_DIR = "D:\\Deployed\\NetworkChat Code\\Network-logs"

def setup_logging():
    now = datetime.datetime.now()
    today_date = datetime.datetime.today().strftime('%d-%m-%y')
    print(f"Current date: {today_date}")
    log_file_name = os.path.join(LOG_DIR, f"alerts_{today_date}.log")
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(level=logging.DEBUG, filename=log_file_name, filemode="w",
                        format="%(asctime)s - %(levelname)s - %(message)s")

def load_last_failure_times():
    last_failure_file = "last_failure_times.json"
    if os.path.exists(last_failure_file):
        with open(last_failure_file, "r") as f:
            return json.load(f)
    else:
        return {}

def save_last_failure_times(times):
    last_failure_file = "last_failure_times.json"
    with open(last_failure_file, "w") as f:
        json.dump(times, f)

def ping_ip(ip):
    try:
        output = subprocess.check_output(["ping", "-n", "1", ip], universal_newlines=True, shell=True, timeout=5)
        if "bytes=32" in output or "ttl" in output:
            print(f"Ping to {ip} at time of {datetime.datetime.now()} ok")
            return True
        else:
            print(f"Ping to {ip} not ok - Output: {output}")
            logging.info(f"Ping to {ip} not ok")
            return False
    except subprocess.TimeoutExpired:
        print(f"Ping to {ip} timed out")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error pinging {ip}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error pinging {ip}: {e}")
        return False

def send_google_chat_message(message, webhook_url):
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    payload = {'text': message}

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        logging.info(f"Message sent successfully to Google Chat: {message}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send message to Google Chat: {e}")

def create_alert_message(alerts):
    return "*Ping Results:*\n\n" + "\n".join(alerts)

def main():
    setup_logging()
    
    #Enter Your network device IP here - which you want to monitor
    ip_addresses = {

         "192.168.201.200": "Test",
         "192.168.201.200": "Test2"
        
    }

    webhook_url = "https://chat.googleapis.com/v1/spaces/AAAAvooQHm4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=xih13VZIPyIfIMNdHLzA-2o4ZukKJ5tsJOFzKxbsoik"

    if not webhook_url:
        logging.error("Google Chat webhook URL is not set.")
        return

    last_failure_times = load_last_failure_times()
    failure_counts = {ip: 0 for ip in ip_addresses}
    last_alert_times = {ip: 0 for ip in ip_addresses}

    while True:
        alerts = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_ip = {executor.submit(ping_ip, ip): ip for ip in ip_addresses}

            for future in future_to_ip:
                ip = future_to_ip[future]
                tag = ip_addresses[ip]
                try:
                    success = future.result()
                    current_time = time.time()

                    if not success:
                        failure_counts[ip] += 1
                        if failure_counts[ip] == 6:  # 3 consecutive failures for real-time alert
                            last_failure_times[ip] = current_time
                            last_alert_times[ip] = current_time
                            save_last_failure_times(last_failure_times)
                            alerts.append(
                                f"*Alerts - Down ⚠️*\nIP : *{ip}*\nName : *{tag}*\nTime : *{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')}*\n")
                            logging.warning(f"Ping to {tag} ({ip}) failed. Sending real-time alert.")
                            print(f"Ping to {tag} ({ip}) failed. Sending real-time alert.")
                        elif failure_counts[ip] > 6 and current_time - last_alert_times[ip] >= 300:  # Periodic alert
                            last_alert_times[ip] = current_time
                            alerts.append(
                                f"*Alerts - Still Down ⚠️*\nIP : *{ip}*\nName : *{tag}*\nTime : *{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')}*\n")
                            logging.warning(f"Ping to {tag} ({ip}) still failing. Sending periodic alert.")
                            print(f"Ping to {tag} ({ip}) still failing. Sending periodic alert.")
                    else:
                        if ip in last_failure_times:
                            del last_failure_times[ip]
                            save_last_failure_times(last_failure_times)
                            alerts.append(
                                f"Alerts - Up ✅\nIP - *{ip}*\nName - *{tag}*\nTime - *{datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')}*\n")
                            logging.info(f"Ping to {tag} ({ip}) has recovered. Sending recovery alert.")
                            print(f"Ping to {tag} ({ip}) has recovered. Sending recovery alert.")
                        failure_counts[ip] = 0

                except Exception as e:
                    logging.error(f"Exception occurred while processing ping for {ip}: {e}")

        if alerts:
            alert_message = create_alert_message(alerts)
            send_google_chat_message(alert_message, webhook_url)

        time.sleep(0.1)

if __name__ == "__main__":
    main()
