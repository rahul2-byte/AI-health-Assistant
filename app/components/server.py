from flask import Flask, request, jsonify
import requests
from pyngrok import ngrok
from dotenv import load_dotenv
import os
import yaml
import re

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_bot_commands():
    # Load YAML file
    with open("./bot-commands.yml", "r", encoding="utf-8") as file:
        bot_commands = yaml.safe_load(file)

    command_dict = {}
    for key, value in bot_commands["commands"].items():
        command_dict[key] = value
    return command_dict

commands = get_bot_commands()

def is_text_a_command(text, commands):
    """Check if the text is command"""
    if re.sub(r"[ /]", "", text) in commands:
        return True
    return False

def text_command(text, commands):
    """ Return the command text"""
    # remove the / and traling spaces from commands
    plain_text_command = re.sub(r"[ /]", "", text)

    if plain_text_command in commands:
        return commands[plain_text_command]
    return "No command found!!"

text_command("/start", commands)

# ✅ Initialize Flask app before defining routes
app = Flask(__name__)

def send_message(chat_id, text):
    """Send message to a specific chat"""
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, json=data)
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming updates from Telegram"""
    update = request.get_json()
    COMMANDS = get_bot_commands()
    
    # Extract message details
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        if "text" in update["message"]:
            received_text = update["message"]["text"]
            # Check for commands in received text
            is_command = is_text_a_command(received_text, COMMANDS)
            
            if is_command:
                command = text_command(received_text, COMMANDS)
                # Send command instruction
                send_message(chat_id, command)
            else: 
                # Echo the received message back to user
                send_message(chat_id, f"You said: {received_text}")
    
    return jsonify({"ok": True})

def setup_webhook(webhook_url):
    """Set up webhook with Telegram"""
    url = f"{BASE_URL}/setWebhook"
    data = {
        "url": webhook_url
    }
    response = requests.post(url, json=data)
    return response.json()

def run_bot():
    # Start ngrok
    PORT = 80
    public_url = ngrok.connect(PORT)
    webhook_url = f"{public_url.public_url}/webhook"

    # Set up webhook with Telegram
    print("Setting up webhook...")
    result = setup_webhook(webhook_url)
    print(f"Webhook setup result: {result}")

    print(f"Webhook URL: {webhook_url}")
    app.run(port=PORT)
    
run_bot()