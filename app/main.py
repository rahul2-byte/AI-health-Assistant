from components.server import TelegramBot

def main():
    
    bot = TelegramBot()
    
    try:
        bot.run()
    except Exception as e: 
        print(f"Error running bot: {e}")

if __name__ == "__main__":
    main()