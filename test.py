import os
import sys
import time
import requests
from colorama import *
from datetime import datetime

red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
black = Fore.LIGHTBLACK_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
reset = Style.RESET_ALL

allToken = 0

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full paths to the files
data_file = os.path.join(script_dir, "data.txt")

# Telegram Bot API endpoint for sending messages
telegram_bot_token = "7223996474:AAHBBXBCRMGM_2S-aGeqydkDfEV508eMRPw"
telegram_chat_id = "6383309781"
telegram_message_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"


class ArixDEX:
    def __init__(self):
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "no-cache",
            "Content-Length": "0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://miner-webapp-pi.vercel.app",
            "Pragma": "no-cache",
            "Priority": "u=1, i",
            "Referer": "https://miner-webapp-pi.vercel.app/",
            "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        }

        self.line = white + "~" * 50

        self.banner = f"""
        {white}ArixDEX Auto Claimer
        
        """

    # Clear the terminal
    def clear_terminal(self):
        # For Windows
        if os.name == "nt":
            _ = os.system("cls")
        # For macOS and Linux
        else:
            _ = os.system("clear")

    def user_info(self, telegram_id):
        url = f"https://miner-webapp-fz9k.vercel.app/api/user?id={telegram_id}"

        headers = self.headers

        response = requests.get(url, headers=headers)

        return response

    def arix_claimer(self, telegram_id):
        url = f"https://miner-webapp-pi.vercel.app/api/claim?id={telegram_id}"

        headers = self.headers

        response = requests.post(url, headers=headers)

        return response

    def send_telegram_message(self, message):
        params = {
            "chat_id": telegram_chat_id,
            "text": message
        }
        response = requests.post(telegram_message_url, params=params)
        return response

    def log(self, msg):
        now = datetime.now().isoformat(" ").split(".")[0]
        print(f"{black}[{now}]{reset} {msg}{reset}")

    def main(self):
        self.clear_terminal()
        print(self.banner)
        data = open(data_file, "r").read().splitlines()
        num_acc = len(data)
        self.log(self.line)
        self.log(f"{green}Number of accounts: {white}{num_acc}")
        
        while True:
            for no, telegram_id in enumerate(data):
                self.log(self.line)
                self.log(f"{green}Account number: {white}{no+1}/{num_acc}")
                try:
                    user_info = self.user_info(telegram_id=telegram_id).json()
                    first_name = user_info["first_name"]
                    last_name = user_info["last_name"]
                    user_name = user_info["username"]
                    tele_id = user_info["id"]
                    balance = user_info["balance"]
                    self.log(
                        f"{green}Account Info: {white}{first_name} {last_name} ({user_name} - {tele_id})"
                    )
                    self.log(f"{green}Balance: {white}{balance}")
                except Exception as e:
                    self.log(f"{red}Get user info error!!!")

                try:
                    claim = self.arix_claimer(telegram_id=telegram_id).json()
                    claim_balance = claim["balance"]
                    self.log(f"{green}Balance after Claim: {white}{claim_balance}")
                    global allToken
                    allToken += claim_balance
                except Exception as e:
                    self.log(f"{red}Claim error!!!")
                
            if allToken >= num_acc:
                # Send Telegram message when all accounts have been claimed
                try:
                    message = f"All accounts have been claimed! Total tokens: {allToken}"
                    self.send_telegram_message(message)
                except Exception as e:
                    self.log(f"{red}Error sending Telegram message!")

            print()
            wait_time = 30 * 60
            self.log(f"{yellow}Waiting for {int(wait_time/60)} minutes!")
            time.sleep(wait_time)


if __name__ == "__main__":
    try:
        arix = ArixDEX()
        arix.main()
        
    except KeyboardInterrupt:
        sys.exit()
