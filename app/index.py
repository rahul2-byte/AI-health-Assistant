import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "python")))
from components.server import TelegramBot
import json

def main(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    bot = TelegramBot(is_local=False)
    
    try:
        # Set up on AWS URL if provided
        aws_url = os.environ.get('AWS_WEBHOOK_URL')
        if aws_url:
            bot.setup_webhook(aws_url)
            # Start the webhook
            bot.webhook()
    except Exception as e: 
        print(f"Error running bot: {e}")
        
    return {"status": "Bot is running"}

if __name__ == "__main__":
    # Run locally
    bot = TelegramBot(is_local=True)
    bot.run_local()