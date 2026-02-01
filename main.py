"""
Splitwise WhatsApp Reminder Bot
Author: Siddh Bhadani
Description: Fetches outstanding balances from Splitwise API and sends 
             automated WhatsApp reminders to friends who owe money.
"""

import os
import sys
import logging
import requests
import pywhatkit
from dotenv import load_dotenv
import time
from typing import Dict, List, Set, Any

# ================== CONFIGURATION & LOGGING ==================

# Setup logging to track successes and failures
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()

# Environment Variables
API_KEY = os.getenv("SPLITWISE_API_KEY")
BASE_URL = "https://secure.splitwise.com/api/v3.0"

# SECURITY: Hard cap to prevent spam
MAX_MESSAGES_PER_RUN = 5
MESSAGE_DELAY_SECONDS = 20  # SECURITY: rate limiting

# Phone number mapping: { "first_name": "phone_number" }
# Ensure phone numbers include the country code (e.g., +1 for Canada/US)
PHONE_BOOK:Dict[str,str] = {
    "dhruvil": "+13065396253",
    # "dhruvil": "+13063513984",
    # "shruti" : "+13065910739",
    # "nency" : "+12269665306",
    # "shubham" : "+13063515391",
    # "kishan" : "+17069888641",
    # "aelis" : "+14036677314",
    # "namra" : "+13065511646",
    # "nikhil" : "+16395548188",
    # "tarang" : "+16479964497",
    # "jimit" : "+16478773878",
}

# ================== VALIDATION ==================

if not API_KEY:
    logging.critical("Invalid or missing SPLITWISE_API_KEY in .env file.")
    sys.exit(1)

# ================== CORE FUNCTIONS ==================

def get_splitwise_friends() -> List[Dict[str, Any]]:
    """Fetches list of friends and their balances from Splitwise API."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(f"{BASE_URL}/get_friends", headers=headers, timeout=10)
        response.raise_for_status()  # Raises error for 4xx or 5xx status codes
        return response.json().get("friends", [])
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to connect to Splitwise API: {e}")
        logging.debug(e)
        return []


def sanitize_message(text: str) -> str:
    """SECURITY: Remove problematic characters for WhatsApp Web."""
    return text.replace('"', "'").strip()

def generate_message(name: str, amount: float, currency: str = "CAD") -> str:
    """Formats the reminder message."""
    return sanitize_message(
        f"Hey {name} 👋\n\n"
        f"Just a quick reminder that you owe me {amount:.2f} {currency} "
        f"from our Splitwise expenses.\n"
        f"Could you please clear it within this week😊??\n\n"
        f"Thanks!"
    )
    
def mask_phone(phone: str) -> str:
    """SECURITY: Avoid logging full phone numbers."""
    return phone[:3] + "****" + phone[-2:]

def send_whatsapp_reminder(phone_no: str, message: str, friend_name: str):
    """Handles the automation of sending a WhatsApp message."""
    try:
        logging.info(f"Attempting to send message to {friend_name} {mask_phone(phone_no)}...")
        # wait_time: seconds to wait before sending (adjust based on internet speed)
        # tab_close: automatically closes the browser tab after sending
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone_no,
            message=message,
            wait_time=20,  # Increased to 20s for better reliability on slower PCs
            tab_close=True,
            close_time=3
        )
        logging.info(f"Successfully queued WhatsApp message for {friend_name}.")

        time.sleep(MESSAGE_DELAY_SECONDS)  # SECURITY: rate limit
    except Exception as e:
        logging.error(f"WhatsApp automation failed for {friend_name}: {e}")
        logging.debug(e)

# ================== MAIN EXECUTION ==================

def main():
    friends = get_splitwise_friends()
    
    if not friends:
        logging.warning("No friends found or API error occurred.")
        return
    
    sent_users: set[str] = set()
    messages_sent = 0

    for friend in friends:
        if messages_sent >= MAX_MESSAGES_PER_RUN:
            logging.info("Message limit reached. Stopping.")
            break

        balances = friend.get("balance", [])
        first_name = (friend.get("first_name") or "").strip()
        last_name = (friend.get("last_name") or "").strip()
        
        if not first_name:
            continue

        name_key = first_name.lower()
        full_name = f"{first_name} {last_name}".strip()

        if name_key in sent_users:
            continue  # SECURITY: no duplicate reminders

        phone_no = PHONE_BOOK.get(name_key)
        if not phone_no:
            logging.warning(f"No phone number for {full_name}.")
            continue
        
        for balance in balances:
            try:
                amount = float(balance.get("amount", 0))
                currency = balance.get("currency_code", "CAD")
                
                if amount > 0:
                    if phone_no:
                        message = generate_message(first_name, amount, currency)
                        send_whatsapp_reminder(phone_no, message, full_name)
                        
                        sent_users.add(name_key)
                        messages_sent += 1
                        break # Only one message per friend
                    else:
                        logging.warning(f"No phone number mapped for {full_name}. Skipping.")
                
            except Exception as e:
                # This will now catch the error and tell you exactly what went wrong
                logging.error(f"Error processing balance for {friend.get('first_name', 'Unknown')}: {e}")

if __name__ == "__main__":
    logging.info("Starting Splitwise Reminder Bot...")
    main()
    logging.info("Process completed.")