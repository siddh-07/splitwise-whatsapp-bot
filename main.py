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
from typing import Dict, List, Any

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

# Phone number mapping: { "first_name": "phone_number" }
# Ensure phone numbers include the country code (e.g., +1 for Canada/US)
PHONE_BOOK = {
    "dhruvil": "+13063513984"
}

if not API_KEY:
    logging.error("SPLITWISE_API_KEY not found in environment variables.")
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
        return []

def generate_message(name: str, amount: float, currency: str = "CAD") -> str:
    """Formats the reminder message."""
    return (
        f"Hey {name} 👋\n\n"
        f"Just a quick reminder that you owe me {amount:.2f} {currency} from our Splitwise expenses.\n"
        f"Whenever you get a chance, please clear it within this week... 😊\n\n"
        f"Thanks!"
    )

def send_whatsapp_reminder(phone_no: str, message: str, friend_name: str):
    """Handles the automation of sending a WhatsApp message."""
    try:
        logging.info(f"Attempting to send message to {friend_name}...")
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
    except Exception as e:
        logging.error(f"WhatsApp automation failed for {friend_name}: {e}")

# ================== MAIN EXECUTION ==================

def main():
    friends = get_splitwise_friends()
    
    if not friends:
        logging.warning("No friends found or API error occurred.")
        return

    for friend in friends:
        # A friend can have multiple balances in different currencies
        balances = friend.get("balance", [])
        
        for balance in balances:
            try:
                amount = float(balance.get("amount", 0))
                currency = balance.get("currency_code", "CAD")
                
                # Logic: Positive amount means they owe YOU.
                if amount > 0:
                    first_name = friend.get("first_name", "").lower()
                    full_name = f"{friend.get('first_name')} {friend.get('last_name')}"
                    
                    phone_no = PHONE_BOOK.get(first_name)
                    
                    if phone_no:
                        msg = generate_message(friend.get('first_name'), amount, currency)
                        send_whatsapp_reminder(phone_no, msg, full_name)
                    else:
                        logging.warning(f"No phone number mapped for {full_name}. Skipping.")
                
                elif amount < 0:
                    logging.info(f"Note: You owe {friend.get('first_name')} {abs(amount)} {currency}.")
            
            except (ValueError, TypeError) as e:
                logging.error(f"Error parsing balance for {friend.get('first_name')}: {e}")

if __name__ == "__main__":
    logging.info("Starting Splitwise Reminder Bot...")
    main()
    logging.info("Process completed.")