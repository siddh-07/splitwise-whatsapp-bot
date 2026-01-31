import sys
from dotenv import load_dotenv
import requests
import os
from twilio.rest import Client

load_dotenv()

# --- ENV VARS ---
API_KEY = os.getenv("SPLITWISE_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")

if not API_KEY:
    print("ERROR: SPLITWISE_API_KEY not found.")
    sys.exit(1)

# --- Twilio Client ---
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# --- Message Generator ---
def generate_message(name, amount):
    return (
        f"Hey {name}, quick reminder 🙂 "
        f"You owe me {amount:.2f} CAD from Splitwise. "
        f"Please clear it when you get a chance. Thanks!"
    )

# --- Send SMS ---
def send_sms(phone_no, message):
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=phone_no
    )

BASE_URL = "https://secure.splitwise.com/api/v3.0"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(f"{BASE_URL}/get_friends", headers=headers)
data = response.json()

index = 0

# --- Your manual phone mapping ---
phone_dict = {
    "dhruvil": "+13063513984",
    "nikhil": "+16395548168",
    "meet" : "+13065396253"
    
}

for friend in data.get("friends", []):
    for balance in friend.get("balance", []):

        amount = float(balance["amount"])
        if amount == 0:
            continue

        name = f"{friend['first_name']} {friend['last_name']}"
        name_key = friend["first_name"].lower()

        if amount > 0:
            
            phone_no = phone_dict.get(name_key)
            if not phone_no:
                print(f"Phone number for {name} not found. Skipping SMS.")
                continue

            message = generate_message(name, amount)
            try:
                send_sms(phone_no, message)
            except Exception as e:
                print(f"SMS failed for {name}: {e}")

            print(f"SMS sent to {name}: {amount} CAD")
        else:
            print(f"I owe {name}: {abs(amount)} {balance['currency_code']}")
