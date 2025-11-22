import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def get_chat_id():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        response = requests.get(url)
        data = response.json()
        
        if not data['ok']:
            print(f"Error: {data['description']}")
            return

        if not data['result']:
            print("No updates found. Please send a message to the bot first.")
            return

        # Get the last message
        last_update = data['result'][-1]
        chat_id = last_update['message']['chat']['id']
        user_name = last_update['message']['from'].get('username', 'Unknown')
        
        print(f"Found Chat ID: {chat_id}")
        print(f"User: {user_name}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_chat_id()
