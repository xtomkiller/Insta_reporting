import requests

def check_access_token(access_token):
    try:
        url = f"https://graph.instagram.com/me?fields=id&access_token={access_token}"
        response = requests.get(url)
        if response.status_code == 200:
            print("Access token is valid and active.")
        else:
            print("Access token is invalid or expired.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the API request: {e}")

# Usage example
access_token = "AOt7yVYJD5fT8aNTd81iFKN"
check_access_token(access_token)
