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

    ip_addresses = {

        # "192.168.201.200": "Test",
        "192.168.200.62": "( AP ) - VEHICLE - HSPLANT - VL - CABIN - 01 - AP - 11 :",
        "192.168.201.234": "( AP ) - VEHICLE - HSPLANT - VL - 02 - AP - 04 :",
        "192.168.201.233": "( AP ) - VEHICLE - HSPLANT - VL - 02 - AP - 03 :",
        "192.168.201.232": "( AP ) - VEHICLE - HSPLANT - VL - 01 - AP - 02 :",
        "192.168.201.231": "( AP ) - VEHICLE - HSPLANT - VL - 01 - AP - 01 :",
        "192.168.201.236": "( AP )- VEHICLE - HSPLANT - STORE - 01 - AP - 06 :",
        "192.168.201.237": "( AP ) - VEHICLE - HSPLANT - REC - 01 - AP - 07 :",
        "192.168.201.240": "( AP ) - VEHICLE - HSPLANT - PDI - 01 - AP - 10 :",
        "192.168.201.239": "( AP ) - VEHICLE - HSPLANT - MEZ - 01 - AP - 09 :",
        "192.168.201.238": "( AP ) - VEHICLE - HSPLANT - MEZ - 01 - AP - 08 :",
        "192.168.201.235": "( AP ) - VEHICLE - HSPLANT - IQC - 01 - AP - 05 :",
        "192.168.200.22": "( AP ) - HSPlant - VL_05_AP - 065 :",
        "192.168.200.20": "( AP ) - HSPlant - VL_03_AP - 063 :",
        #"192.168.200.18": "( AP ) - HSPlant - VL_01_AP - 061 :",
        # "192.168.200.30": "( AP ) - HSPlant - TR_01_AP - 073 :",
        "192.168.200.33": "( AP ) - HSPlant - ST_02_AP - 076 :",
        "192.168.200.32": "( AP ) - HSPlant - ST_01_AP - 075 :",
        "192.168.200.35": "( AP ) - HSPlant - SF_01_AP - 078 :",
        "192.168.200.28": "( AP ) - HSPlant - REC_01_AP - 071 :",
        "192.168.201.250": "( AP ) - HsPlant - Protolab - 84 :",
        "192.168.200.39": "( AP ) - HSPlant - PL_01_AP - 082 :",
        "192.168.200.192": "( AP ) - HSPLANT - MZ - 01 - AP - 15 :",
        "192.168.200.252": "( AP ) - HSPLANT - MZ - 01 - AP - 14 :",
        "192.168.200.251": "( AP ) - HSPLANT - MZ - 01 - AP - 13 :",
        "192.168.200.38": "( AP ) - HSPlant - MEZ_02_AP - 081 :",
        "192.168.200.40": "( AP ) - HSPlant - MEZ_01_AP - 080 :",
        "192.168.200.31": "( AP ) - HSPlant - IQC_01_AP - 074 :",
        "192.168.200.36": "( AP ) - HSPlant - FG_01_AP - 079 :",
        "192.168.200.27": "( AP ) - HSPlant - CR_02_AP - 070 :",
        "192.168.200.26": "( AP ) - HSPlant - CR_01_AP - 069 :",
        "192.168.200.29": "( AP ) - HSPlant - CAF_01_AP - 072 :",
        "192.168.200.25": "( AP ) - HSPlant - BL_03_AP - 068 :",
        "192.168.200.24": "( AP ) - HSPlant - BL_02_AP - 067 :",
        "192.168.200.23": "( AP ) - HSPlant - BL_01_AP - 066 :",

        "192.168.200.85": "SWITCH - AE - SW - 082:",
        "192.168.200.86": "SWITCH - AE - SW - 083:",
        "192.168.200.87": "SWITCH - AE - SW - 084:",
        # "192.168.200.88":  "SWITCH - AE - SW - 085:",
        # "192.168.200.89":  "SWITCH - AE - SW - 086:",
        "192.168.200.4": "SWITCH - HSPlant - Access - BL_01_SW_039:",
        "192.168.200.3": "SWITCH - HSPlant - Access - BL_02_SW_040:",
        "192.168.200.2": "SWITCH - HSPlant - Access - BL_03_SW_041:",
        "192.168.201.214": "SWITCH - HSPlant - Access - BL_E - Line_SW_01:",
        "192.168.200.5": "SWITCH - HSPlant - Access - BL_G - Line_SW_044:",
        "192.168.200.7": "SWITCH - HSPlant - Access - BL_G - Line_SW_42:",
        "192.168.200.6": "SWITCH - HSPlant - Access - BL_G - Line_SW_43:",
        "192.168.200.10": "SWITCH - HSPlant - Access - CR_01_SW_045:",
        "192.168.200.8": "SWITCH - HSPlant - Access - CR_03_SW_047:",
        "192.168.200.15": "SWITCH - HSPlant - Access - SR_02_SW_052:",
        "192.168.200.16": "SWITCH - HSPlant - Access - SR_03_SW_053:",
        "192.168.200.12": "SWITCH - HSPlant - Access - ST_02_SW_049:",
        "192.168.201.218": "SWITCH - HSPlant - Access - ST_SW_048:",
        # "10.10.200.8":    "SWITCH - HSPlant - MS390Core - SR_01_CSW - 03:",
        # "10.10.200.8":    "SWITCH - HSPlant - MS390Core - SR_02_CSW - 04:",
        "192.168.201.203": "SWITCH - NewHSPlant - Access - Doc - 1 - SW - 09:",
        "192.168.201.206": "SWITCH - NewHSPlant - Access - Dyno - 1 - SW - 12:",
        "192.168.201.207": "SWITCH - NewHSPlant - Access - FG - 1 - SW - 13:",
        "192.168.201.210": "SWITCH - NewHSPlant - Access - IQC - 1 - SW - 14:",
        "192.168.201.205": "SWITCH - NewHSPlant - Access - PDI - 1 - SW - 11:",
        "192.168.201.202": "SWITCH - NewHSPlant - Access - PH - 1 - SW - 10:",
        "192.168.201.213": "SWITCH - NewHSPlant - Access - SR - 1 - SW - 03:",
        "192.168.201.217": "SWITCH - NewHSPlant - Access - SR - 1 - SW - 04:",
        "192.168.201.204": "SWITCH - NewHSPlant - Access - VL - 1 - SW - 07:",
        "192.168.201.201": "SWITCH - NewHSPlant - Access - VL - 1 - SW - 08:",
        "192.168.201.215": "SWITCH - NewHSPlant - Access - VL - 1 - SW - 15:",
        "192.168.201.208": "SWITCH - NewHSPlant - Access - VL - 2 - SW - 05:",
        "192.168.201.209": "SWITCH - NewHSPlant - Access - VL - 2 - SW - 06:",
        "192.168.201.216": "SWITCH - NewHSPlant - Access - VL - 2 - SW - 16:",
        "192.168.201.211": "SWITCH - NewHSPlant - CORE - SR - 1 - SW - 01:",
        "192.168.201.212": "SWITCH - NewHSPlant - CORE - SR - 1 - SW - 02:",
        "192.168.200.66": "( AP ) - Test AP 1:",
        "192.168.200.67": "( AP ) - Test AP 2:"

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
