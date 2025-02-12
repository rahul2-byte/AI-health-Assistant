import logging
from telegram import Update
from dotenv import load_dotenv
import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext
)

from components.agents import llmchain

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class Bot:
    
    def __init__(self):
        load_dotenv()
        self.app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
        
    COMMANDS = {
            "start": '''
👋 Welcome to HealthMate! 🤖💙  
Your AI-powered health assistant is here to guide you on your wellness journey!  

💡 What I can do for you:  
✅ Personalized health & nutrition tips  
✅ Exercise & mental wellness support  
✅ Daily health insights  

Type /help to explore all my features! 🚀
                ''',

            "help": '''
📖 HealthMate Help Center 🏥  

Here are my available commands:  

🔹 /nutrition - Healthy eating tips 🍏  
🔹 /exercise - Quick workout guides 🏃‍♂️  
🔹 /mentalhealth - Mindfulness & stress relief 🧘‍♀️  
🔹 /healthtip - Daily health wisdom 💡  
🔹 /faq - Common questions answered ❓  
🔹 /contact - Reach out for more support 📞  
🔹 /settings - Customize your experience ⚙️  

💙 Type any command to explore its features!
            ''',

            "info" : '''
👨‍⚕️ About HealthMate 🤖  
I’m e to provide AI-powered health guidance!  
📌 I p with nutrition, fitness, mental wellness, and more.  
📌 I or daily tips & insights to support your well-being.  
📌 Disclar: My advice is informational, not a substitute for a doctor! 
💡 Need help? Type /help to explore commands.
            ''',

            "nutritions" : '''
🥗 Let’s Talk Nutrition! 🍽️  

Eating healthy is the key to a strong body! Here’s a tip for today:  
💡 "Include more fiber-rich foods like whole grains, fruits, and veggies for better digestion!" 🌾🍏  

Want meal ideas or personalized tips? Choose an option below:  
🔹 /mealplan - Get a balanced meal plan 🍱  
🔹 /healthyrecipes - Try delicious, healthy recipes 🥑  
🔹 /hydration - Learn about the importance of water 💦  
            ''',

            "exercise" : '''
🏋️‍♂️ Time to Get Active! 🏃‍♀️  
Physical activity keeps you fit and energized! Here’s a quick workout:  
🔥 Warm-up: 5 minutes of stretching  
🔥 Workout: 15 squats + 10 push-ups + 30-second plank  

Want more? Pick your style:  
🔹 /homeworkout - No-equipment workouts 🏠  
🔹 /cardio - Heart-pumping exercises ❤️  
🔹 /strength - Build muscle and endurance 💪  
            ''',

            "mentalhealth" : '''
🧘‍♀️ Mental Wellness Matters! 🌿  

Taking care of your mind is just as important as your body. Here’s a mindfulness tip:  
💡 "Pause for a moment. Take a deep breath in... hold... and slowly exhale. Repeat 5 times." 🌬️  

Want more? Explore:  
🔹 /stressrelief - Quick ways to reduce stress 😌  
🔹 /meditation - Short guided meditation sessions 🎧  
🔹 /positivity - Boost your mood with affirmations 💙  
            ''',
            
            "healthtip" : '''
📢 Health Tip of the Day! 🌟  

💡 "A 10-minute walk after meals can improve digestion and lower blood sugar levels!" 🚶‍♂️  

👉 Want more tips? Just type /healthtip again!  
            ''',
            
            "faq" : '''
📌 Frequently Asked Questions  

🔹 Q: Can you diagnose my health condition?  
❌ No, I provide general advice but can’t replace a doctor.  

🔹 Q: How often should I exercise?  
✅ At least 30 minutes a day, 5 times a week is great!  

🔹 Q: Can you suggest a diet plan?  
🍎 Yes! Try /nutrition for meal ideas.  

💡 Need more help? Type /contact to reach out! 📞
            ''',
            
            "contact": '''
📞 Need Professional Support? 🏥  

🚑 For medical emergencies, contact your local healthcare provider immediately!  

💙 Helpful Resources:  
📌 General Health Advice: [WHO Website](https://www.who.int) 🌍  
📌 Mental Health Support: [Mind.org](https://www.mind.org.uk) 🌿  

💡 Have feedback? Message the bot developer at @YourBotSupport  
            ''',

        "settings": '''
⚙️ Bot Settings Menu  

🔧 Adjust your preferences:  
1️⃣ Change Language 🌍  
2️⃣ Set Daily Health Tip Timing ⏰  
3️⃣ Enable/Disable Notifications 🔔  

💡 Type /settings option_name to update your preferences!  
            '''
    }

    async def message_handler(self, update: Update, context: CallbackContext):

        """Handles all non-command text messages"""
        user_message = update.message.text
        user_name = update.message.from_user.first_name

        # reply_text = f"Hello {user_name}, you said: {user_message}"
        output = llmchain.get_output(user_message)
        await update.message.reply_text(f"Hello {user_name}, Your answer: {output}")
        
    def bot_commands(self):

        # Register command handlers
        async def command_handler(update: Update, context: CallbackContext):
            command = update.message.text.lstrip("/")
            response = self.COMMANDS.get(command, "❌ Command not found!")
            print("Registering Response:", response)
            await update.message.reply_text(response)

        for command in self.COMMANDS.keys():
            self.app.add_handler(CommandHandler(command, command_handler))

        # Register message handler for any text that is NOT a command
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))

    def run(self):
        self.bot_commands()
        self.app.run_polling()