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
    def __init__(self, is_local=False):
        self.is_local = is_local
        # Load environment variables based on environment
        if self.is_local:
            load_dotenv()
            self.BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
            self.PORT = int(os.getenv("PORT", 80))
        else:
            self.BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
        
        self.BASE_URL = f"https://api.telegram.org/bot{self.BOT_TOKEN}"
        
        # ✅ Initialize Flask app before defining routes
        self.app = Flask(__name__)
        self.commands = self.get_bot_commands()
        
        # Register the webhook route
        self.app.route('/webhook', methods=['POST'])(self.webhook)

    def get_bot_commands(self):
        try:
            # Adjust path based on environment
            if self.is_local:
                commands_path = "components/bot-commands.yml"
            else:
                commands_path = os.path.join(os.getcwd(), "bot-commands.yml")
                # If file is not found than raise the error
                if not os.path.exists(commands_path):
                    raise FileNotFoundError(f"File not found: {commands_path}")

            with open(commands_path, "r", encoding="utf-8") as file:
                bot_commands = yaml.safe_load(file)
            return {key: value for key, value in bot_commands["commands"].items()}
        except Exception as e:
            print(f"Error loading bot commands: {str(e)}")
            return {}

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
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return {"ok": False, "error": str(e)}

    def webhook(self):
        """Handle incoming updates from Telegram"""
        try:
            update = request.get_json()
            
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                if "text" in update["message"]:
                    received_text = update["message"]["text"]

                    if self.is_text_a_command(received_text, self.commands):
                        command = self.text_command(received_text, self.commands)
                        self.send_message(chat_id, command)
                    else: 
                        output = llmchain.get_output(received_text)
                        self.send_message(chat_id, f"You said: {output}")

            return jsonify({"ok": True})
        except Exception as e:
            print(f"Error in webhook: {str(e)}")
            return jsonify({"ok": False, "error": str(e)})

    def setup_webhook(self, webhook_url):
        """Set up webhook with Telegram"""
        url = f"{self.BASE_URL}/setWebhook"
        data = {
            "url": webhook_url
        }
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            print(f"Webhook setup response: {response.json()}")
            return response.json()
        except Exception as e:
            print(f"Error setting up webhook: {str(e)}")
            return {"ok": False, "error": str(e)}
    
    def run_local(self):
        """Run the bot locally using ngrok"""
        try:
            from pyngrok import ngrok
            
            public_url = ngrok.connect(self.PORT)
            webhook_url = f"{public_url.public_url}/webhook"
            
            print("Setting up webhook for local development...")
            result = self.setup_webhook(webhook_url)
            
            if result.get("ok"):
                print(f"Local Webhook URL: {webhook_url}")
                self.app.run(port=self.PORT)
            else:
                print("Failed to set up webhook")
                
        except Exception as e:
            print(f"Error in local run: {str(e)}")
            return {"status": 500, "error": str(e)}
            
        return {"status": 200, "data": "Bot is Running"}