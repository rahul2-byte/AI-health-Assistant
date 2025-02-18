import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "python")))

from flask import Flask, request, jsonify
import requests
from pyngrok import ngrok
from dotenv import load_dotenv
import yaml
import re
from components.agents import llmchain

class TelegramBot():
    def __init__(self):
        self.PORT = 80
        load_dotenv()
        BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
        self.BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
        
        # ✅ Initialize Flask app before defining routes
        self.app = Flask(__name__)
        self.commands = self.get_bot_commands()
        
        # Register the webhook route
        self.app.route('/webhook', methods=['POST'])(self.webhook)

    def get_bot_commands(self):
        # Load YAML file
        with open("app/components/bot-commands.yml", "r", encoding="utf-8") as file:
            bot_commands = yaml.safe_load(file)
        # Return the bot commands
        return {key: value for key, value in bot_commands["commands"].items()}

    @staticmethod
    def is_text_a_command(text, commands):
        """Check if the text is command"""
        return re.sub(r"[ /]", "", text) in commands

    @staticmethod
    def text_command(text, commands):
        """ Return the command text"""
        plain_text_command = re.sub(r"[ /]", "", text)

        return commands.get(plain_text_command, "No command found!!")

    def send_message(self, chat_id, text):
        """Send message to a specific chat"""
        url = f"{self.BASE_URL}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text
        }
        response = requests.post(url, json=data)
        return response.json()

    def webhook(self):
        """Handle incoming updates from Telegram"""
        update = request.get_json()
        
        # Extract message details
        if "message" in update:
            chat_id = update["message"]["chat"]["id"]
            if "text" in update["message"]:
                received_text = update["message"]["text"]
                # Check for commands in received text

                if self.is_text_a_command(received_text, self.commands):
                    command = self.text_command(received_text, self.commands)
                    # Send command instruction
                    self.send_message(chat_id, command)
                else: 
                    # Echo the received message back to user
                    output = llmchain.get_output(received_text)
                    self.send_message(chat_id, f"You said: {output}")

        return jsonify({"ok": True})

    def setup_webhook(self, webhook_url):
        """Set up webhook with Telegram"""
        url = f"{self.BASE_URL}/setWebhook"
        data = {
            "url": webhook_url
        }
        response = requests.post(url, json=data)
        return response.json()

    def run(self):
        public_url = ngrok.connect(self.PORT)
        webhook_url = f"{public_url.public_url}/webhook"

        # Set up webhook with Telegram
        print("Setting up webhook...")
        result = self.setup_webhook(webhook_url)
        print(f"Webhook setup result: {result}")

        print(f"Webhook URL: {webhook_url}")
        self.app.run(port=self.PORT)
        
        return {"status": 200, "data": "Bot is Running"}