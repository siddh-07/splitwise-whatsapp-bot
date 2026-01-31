import sys
from dotenv import load_dotenv
import requests
import os
import pywhatkit  # WhatsApp Web automation

load_dotenv()

# --- ENV VARS ---
API_KEY = os.getenv("SPLITWISE_API_KEY")

if not API_KEY:
    print("ERROR: SPLITWISE_API_KEY not found.")
    sys.exit(1)

# --- Message Generator ---
def generate_message(name, amount):
    return (
        f"Hey {name} 👋\n"
        f"Just a quick reminder that you owe me {amount:.2f} CAD from our Splitwise expenses.\n"
        f"Whenever you get a chance, please clear it within this Week... 😊\n"
        f"Thanks!"
    )

BASE_URL = "https://secure.splitwise.com/api/v3.0"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(f"{BASE_URL}/get_friends", headers=headers)
data = response.json()

# --- Your manual phone mapping ---
phone_dict = {
    "dhruvil": "+13063513984"
}

for friend in data.get("friends", []):
    for balance in friend.get("balance", []):
        amount = float(balance["amount"])
        if amount == 0:
            continue

        name = f"{friend['first_name']} {friend['last_name']}"
        name_key = friend["first_name"].lower()

        if amount > 0:  # they owe you
            phone_no = phone_dict.get(name_key)
            if not phone_no:
                print(f"Phone number for {name} not found. Skipping WhatsApp message.")
                continue

            message = generate_message(name, amount)
            try:
                # Send via WhatsApp Web instantly
                pywhatkit.sendwhatmsg_instantly(
                    phone_no=phone_no,
                    message=message,
                    wait_time=10,   
                    tab_close=True 
                )
            except Exception as e:
                print(f"WhatsApp message failed for {name}: {e}")
                continue

            print(f"WhatsApp message ready for {name}: {amount} CAD")
        else:
            print(f"I owe {name}: {abs(amount)} {balance['currency_code']}")
