from components.server import TelegramBot

def main():
    
    bot = TelegramBot()
    
    try:
        bot.run()
    except Exception as e: 
        print(f"Error running bot: {e}")
        
    return {"status": "Bot is running"}