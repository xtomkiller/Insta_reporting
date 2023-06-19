import os
import sys
import json
import requests
import itertools
import threading
from requests.exceptions import RequestException, ProxyError, Timeout

# Replace the placeholder values with your actual configuration data
__config__ = {
    "username": "<your_username>",
    "password": "<your_password>",
    "target": "<target_username>",
    "reason_id": "<reason_id>",
    "count": 10
}

class Thanatos:
    def __init__(self):
        if sys.platform == "linux":
            os.system("clear")
        else:
            os.system("cls && title 𝙏𝙝𝙖𝙣𝙖𝙩𝙤𝙨 ^| github.com/Plasmonix")
        
        self.sent = 0
        self.errors = 0
        self.proxies = itertools.cycle(open('./data/proxies.txt').read().splitlines())
        self.client = requests.Session()

    def login(self):
        headers = {
            # Replace with your actual headers
        }

        payload = {
            # Replace with your actual payload
        }

        use_tor_proxy = __config__.get("tor")  # Check if tor proxy is enabled
        proxy = None

        if use_tor_proxy:
            proxy = "socks5://localhost:9050"

        try:
            res = self.client.post(
                "https://www.instagram.com/accounts/login/ajax/",
                headers=headers,
                data=payload,
                proxies={"https": proxy} if proxy else None,
                timeout=5
            )

            if res.status_code == 200 and '"authenticated":true' in res.text:
                print(f"[\x1b[32m+\x1b[0m] Successfully logged into {__config__['username']}")
                self.client.headers.update({"x-csrftoken": res.cookies["csrftoken"]})

                profile = self.client.get(
                    f"https://i.instagram.com/api/v1/users/web_profile_info/?username={__config__['target']}",
                    headers={"user-agent": "Instagram 85.0.0.21.100 Android (23/6.0.1; 538dpi; 1440x2560; LGE; LG-E425f; vee3e; en_US)"},
                    proxies={"https": proxy} if proxy else None,
                    timeout=5
                )

                user_id = str(profile.json()["data"]["user"]["id"])
                for _ in range(__config__["count"]):
                    try:
                        threading.Thread(target=self.report, args=(user_id,)).start()
                    except Exception as err:
                        print(err)

            elif res.status_code == 200 and '"user":false' in res.text:
                print(f"[\x1b[31m!\x1b[0m] Username does not exist")

            elif res.status_code == 200 and 'showAccountRecoveryModal' in res.text:
                print(f"[\x1b[31m!\x1b[0m] Incorrect password")

            elif res.status_code == 200 and '"message":"checkpoint_required"' in res.text:
                print(f"[\x1b[31m!\x1b[0m] 2FA enabled")

            else:
                print(f"[\x1b[31m!\x1b[0m] {res.text}")

        except Exception as err:
            print(f"[\x1b[31m!\x1b[0m] {err}")

    def report(self, user_id):
        try:
            data = {
                "source_name": "",
                "reason_id": __config__["reason_id"],
                "frx_contex": ""
            }
            proxy = next(self.proxies, None)  # Get next proxy from the cycle or None if no more proxies available
            req = self.client.post(
                f"https://www.instagram.com/users/{user_id}/report/",
                data=data,
                proxies={"https": proxy} if proxy else None,
                timeout=5
            )

            if req.status_code == 200 and '"status":"ok"' in req.text:
                self.sent += 1
                print(f"[\x1b[34m*\x1b[0m] Sent: {self.sent} | Errors: {self.errors}")
            else:
                self.errors += 1
                print(f"[\x1b[34m*\x1b[0m] Sent: {self.sent} | Errors: {self.errors}")

        except RequestException as err:
            print(f"[\x1b[31m!\x1b[0m] {err}")
            self.report(user_id)  # Retry report

            # Skip non-working proxy
            if proxy:
                print(f"[\x1b[31m!\x1b[0m] Proxy {proxy} is not working. Skipping...")
                self.report(user_id)  # Retry report without proxy

        except (ProxyError, Timeout) as err:
            print(f"[\x1b[31m!\x1b[0m] {err}")
            self.report(user_id)  # Retry report without proxy

if __name__ == "__main__":
    client = Thanatos()
    client.login()
