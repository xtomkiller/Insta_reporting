import requests

class Thanatos:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_user_id(self, username):
        try:
            url = f"https://graph.instagram.com/v13.0/{username}?fields=id&access_token={self.access_token}"
            response = requests.get(url)
            response_json = response.json()
            print(response_json)  # Print the response for debugging
            if "id" in response_json:
                return response_json["id"]
            else:
                print(f"Unable to retrieve user ID for '{username}'.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the API request: {e}")
            return None

    def report_account(self, account_id, reason):
        try:
            url = f"https://graph.instagram.com/{account_id}/restricted"
            headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/x-www-form-urlencoded"}
            data = {"access_token": self.access_token, "reason": reason}
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                print("Account reported successfully.")
            else:
                print(f"Error occurred while reporting the account: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the API request: {e}")

    def select_reason(self):
        print("Select a reason:")
        print("1. Spam")
        print("2. Harassment")
        print("3. Impersonation")
        print("4. Intellectual Property")
        print("5. Nudity")
        while True:
            selected_code = input("Enter the reason code or press 'Q' to quit: ")
            if selected_code.upper() == "Q":
                return None
            if selected_code in ["1", "2", "3", "4", "5"]:
                return selected_code
            print("Invalid reason code. Please try again.")

    def main(self):
        account_name = input("Enter the account name to report: ")
        reason = self.select_reason()
        if reason is not None:
            account_id = self.get_user_id(account_name)
            if account_id is not None:
                self.report_account(account_id, reason)
            else:
                print("Account not found.")

if __name__ == "__main__":
    access_token = "IGQVJWZAFpZAME9mWEtudVNRNkZAQNF9hWFhOckZAqWktoWTZArY3ZAUeGd0d1AwN2hNZAEY3LU9QTXlXa0JLY2dmNDE4emtHbzdRcDVVN2hheXIyTWdPaWZAUSmZAyNEtnRGtZAclI3ZAENqcFdwcXo2TmR2Y1BKSwZDZD"
    thanatos = Thanatos(access_token)
    thanatos.main()
