import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "python")))

from components.server import TelegramBot
import json

def main(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    bot = TelegramBot()
    
    try:
        bot.run()
    except Exception as e: 
        print(f"Error running bot: {e}")
        
    return {"status": "Bot is running"}