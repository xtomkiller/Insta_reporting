import os
import sys
import json
import requests
import itertools
import threading

__config__ = json.load(open('./data/config.json', 'r+'))

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
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-length": "267",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "ig_did=0897491F-B736-4E7E-A657-37438D0967B8; csrftoken=xvAQoMiz2eaU4RrcmRp2hqinDVMfgkpe; rur=FTW; mid=XxTPfgALAAGHGReE-x_i1ISMG4Xr",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": f"Mozilla/91.81 (Linux; Android 6.3; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36",
            "x-csrftoken": "xvAQoMiz2eaU4RrcmRp2hqinDVMfgkpe",
            "x-ig-app-id": "1217981644879628",
            "x-ig-www-claim": "0",
            "x-instagram-ajax": "180c154d218a",
            "x-requested-with": "XMLHttpRequest"
        }

        payload = {
            "username": f"{__config__['username']}",
            "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:&:{__config__['password']}",
        }

        proxy = None
        if __config__.get('use_proxy'):
            proxy = f"http://{next(self.proxies)}"

        try:
            res = self.client.post(
                "https://www.instagram.com/accounts/login/ajax/",
                headers=headers,
                data=payload,
                proxies={"https": proxy},
                timeout=5
            )

            if res.status_code == 200 and '"authenticated":true' in res.text:
                print(f"[\x1b[32m+\x1b[0m] Successfully logged into {__config__['username']}")
                self.client.headers.update({"x-csrftoken": res.cookies["csrftoken"]})

                profile = self.client.get(
                    f"https://i.instagram.com/api/v1/users/web_profile_info/?username={__config__['target']}",
                    headers={'user-agent': 'Instagram 85.0.0.21.100 Android (23/6.0.1; 538dpi; 1440x2560; LGE; LG-E425f; vee3e; en_US'},
                    proxies={"https": proxy} if proxy else None,
                    timeout=5
                )

                user_id = str(profile.json()["data"]["user"]["id"])
                for _ in range(__config__['count']):
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

        except requests.exceptions.RequestException as err:
            print(f"[\x1b[31m!\x1b[0m] {err}")
            self.login()  # Retry login

            # Skip non-working proxy
            if proxy:
                print(f"[\x1b[31m!\x1b[0m] Proxy {proxy} is not working. Skipping...")
                self.login()  # Retry login without proxy

    def report(self, user_id):
        try:
            data = {
                "source_name": "",
                "reason_id": f"{__config__['reason_id']}",
                "frx_contex": ""
            }
            req = self.client.post(
                f"https://www.instagram.com/users/{user_id}/report/",
                data=data,
                proxies={"https": f"http://{next(self.proxies)}"} if __config__.get('use_proxy') else None,
                timeout=5
            )

            if req.status_code == 200 and '"status":"ok"' in req.text:
                self.sent += 1
                print(f"[\x1b[34m*\x1b[0m] Sent: {self.sent} | Errors: {self.errors}")
            else:
                self.errors += 1
                print(f"[\x1b[34m*\x1b[0m] Sent: {self.sent} | Errors: {self.errors}")

        except requests.exceptions.RequestException as err:
            print(f"[\x1b[31m!\x1b[0m] {err}")
            # You can handle the specific error here, if needed

if __name__ == "__main__":
    client = Thanatos()
    client.login()
