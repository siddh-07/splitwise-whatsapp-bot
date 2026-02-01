# Splitwise WhatsApp Reminder Bot 🤖💸

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Splitwise WhatsApp Reminder Bot** is a Python-based automation tool that helps you recover lent money without the awkward "hey, you owe me" conversation. It connects to the Splitwise API to fetch outstanding balances and automatically sends a polite, personalized reminder to your friends via WhatsApp.

---

## 🚀 Features

-   **Real-time Balance Sync:** Fetches the most recent "You are owed" data directly from Splitwise.
-   **Automated Messaging:** Uses `pywhatkit` to automate WhatsApp Web messaging.
-   **JSON Data Management:** Keep your contact list separate from your code using a dedicated friends.json file.
-   **Anti-Spam Protection:** Built-in rate limiting and message caps to ensure safe automation.
-   **Smart Mapping:** Maps Splitwise names to phone numbers via a configurable dictionary.
-   **Currency Aware:** Automatically detects and mentions the currency (CAD, USD, INR, etc.) of the debt.
-   **Privacy Focused:** Automatically masks phone numbers in console logs and keeps sensitive data out of the source code.

---

## 🛠️ Prerequisites

Before running this bot, ensure you have the following:

1.  **Python 3.8+** installed on your system.
2.  **Splitwise API Key:**
    -   Go to [Splitwise Apps](https://secure.splitwise.com/apps/new).
    -   Register a new application to get your **API Key (Personal Access Token)**.
3.  **WhatsApp Web:**
    -   You must be logged into [WhatsApp Web](https://web.whatsapp.com/) in your default browser (Chrome/Edge/Firefox).

---

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/splitwise-whatsapp-bot.git
    cd splitwise-whatsapp-bot
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Environment Variables:**
    Create a `.env` file in the root directory:
    ```env
    SPLITWISE_API_KEY=your_actual_token_here
    ```

4.  **Configure your friends list:**
    Create `friends.json` file in the root directory: 
    ```JSON
    PHONE_BOOK = {
        "Alex": "+13479537392",
        "john": "+1234567890"
    }
    ```

---

## 🚀 Usage

Simply run the script:
```bash
python main.py
```

**Note:** The script will open a browser tab for each message. It will wait for a few seconds (default 20s) to allow WhatsApp Web to load before typing and sending the message automatically.

---

## 📁 Project Structure

```text
├── main.py              # Main logic & API handling
├── friends.json         # Contact mapping (Create this manually)
├── .env                 # API Keys (DO NOT UPLOAD TO GITHUB)
├── .gitignore           # Protects sensitive files from being public
├── requirements.txt     # List of dependencies
└── README.md            # Project documentation
```

---

## 🛡️ Security Note

**Never commit your `.env` file!** This project uses `python-dotenv` to keep your API keys safe locally. The `.gitignore` file is pre-configured to ignore `.env` to prevent accidental leaks of your Splitwise credentials.

---

## 🗺️ Roadmap & Future Improvements

-   [ ] **Database Support:** Store phone numbers in a SQLite database instead of a hardcoded dictionary.
-   [ ] **Headless Messaging:** Integrate with the Twilio API for background messaging without opening a browser.
-   [ ] **Automatic Scheduling:** Add a feature to run the bot automatically every weekend.
-   [ ] **Multi-Currency Totaling:** Convert all debts to a base currency (like CAD) using a live exchange rate API.

---

## 👤 Author

**Siddh Bhadani**
-   GitHub: [@Siddh07](https://github.com/siddh-07)
-   LinkedIn: [Siddh Bhadani](https://www.linkedin.com/in/bhadani-siddh-15953a249/)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

***