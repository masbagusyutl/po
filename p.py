import requests
import time
import json
from datetime import datetime, timedelta
from colorama import init, Fore, Style

# Initialize colorama
init()

# Fungsi untuk membuat GET request
def make_get_request(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(Fore.RED + f"Request failed with status code {response.status_code}")
        return None

# Fungsi untuk menghitung mundur 12 jam dengan tampilan waktu yang bergerak
def countdown_timer(hours):
    end_time = datetime.now() + timedelta(hours=hours)
    while datetime.now() < end_time:
        remaining_time = end_time - datetime.now()
        print(Fore.YELLOW + f"Time remaining: {str(remaining_time).split('.')[0]}", end="\r")
        time.sleep(1)
    print(Fore.GREEN + "Countdown completed!")

# Baca data.txt untuk mendapatkan Authorization tokens
def read_tokens(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

# Main function
def main():
    url_info = "https://moon.popp.club/moon/asset"
    url_farming = "https://moon.popp.club/moon/farming"
    tokens = read_tokens('data.txt')
    total_accounts = len(tokens)
    print(Fore.CYAN + f"Total accounts: {total_accounts}")

    while True:
        for index, token in enumerate(tokens, start=1):
            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
                "Authorization": f"Bearer {token}",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "application/json;charset=utf-8",
                "Host": "moon.popp.club",
                "Origin": "https://planet.popp.club",
                "Pragma": "no-cache",
                "Referer": "https://planet.popp.club/",
                "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-site",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
            }

            # Get info data
            print(Fore.BLUE + f"Processing account {index}/{total_accounts}")
            info_data = make_get_request(url_info, headers)
            if info_data:
                points = info_data.get("sd", 0)
                print(Fore.GREEN + f"Account {index} points: {points}")

            # Perform farming task
            farming_data = make_get_request(url_farming, headers)
            if farming_data:
                print(Fore.GREEN + f"Farming task completed for account {index}")

            # Jeda 5 detik antar akun
            time.sleep(5)

        # Hitung mundur 12 jam
        countdown_timer(12)

if __name__ == "__main__":
    main()
