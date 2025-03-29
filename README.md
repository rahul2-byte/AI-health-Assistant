# AI Health Agent

A Telegram-based conversational health assistant powered by large language models that provides fitness tracking, nutrition advice, and mental health support.

## 📱 Overview

AI Health Agent is a chatbot that leverages advanced language models to help users maintain and improve their health through natural conversation. The agent is accessible through Telegram, making it easy to integrate into users' daily routines.

## ✨ Features

- **Fitness Tracking**: Log workouts, track progress, and receive personalized exercise recommendations
- **Nutrition Advice**: Get meal suggestions, nutritional information, and dietary guidance
- **Mental Health Support**: Access stress management techniques, mood tracking, and mindfulness exercises
- **Natural Conversation**: Interact with the agent using everyday language through Telegram

## 🖼️ Screenshots & Demo

![image](https://github.com/user-attachments/assets/dc788f4a-3af9-44da-bac9-e28f6ed17d86)

![image](https://github.com/user-attachments/assets/cc9a0728-537a-415f-a1fa-c0dd466bb176)

<!-- Screenshots and demo content will be added here -->

## 🛠️ Technology Stack

- **Large Language Models**: Deepseek powers the natural language understanding and generation capabilities of the bot
- **Python**: Core programming language for the application logic
- **AWS Lambda**: Cloud infrastructure for scalable, serverless deployment
- **Telegram Bot API**: Interface for user interaction

## 🚀 Getting Started

### Prerequisites

- A Telegram account

### Usage

1. Access the AI Health Agent on Telegram by clicking [this link](https://t.me/MediHelp_ChatBot)
2. Start a conversation with the bot
3. Ask health-related questions or use commands to track fitness, get nutrition advice, or access mental health resources

### Example Interactions

```
You: How many calories are in an apple?

AI Health Agent: A medium-sized apple (about 182 grams) contains approximately 95 calories. 
Apples are also rich in fiber, vitamin C, and various antioxidants, making them a nutritious snack option!
```

```
You: I'm feeling stressed about work

AI Health Agent: I'm sorry to hear you're feeling stressed. Here are some quick techniques that might help:

1. Take 5 deep breaths, inhaling for 4 counts and exhaling for 6
2. Try a 5-minute mindfulness exercise where you focus only on your immediate surroundings
3. Consider a short walk to clear your mind

Would you like me to guide you through a quick relaxation exercise?
```

## ⚙️ Technical Implementation

The AI Health Agent uses a serverless architecture with AWS Lambda functions that process incoming messages from the Telegram Bot API. The system analyzes user messages using large language models to understand intent and generate helpful, contextually appropriate responses.

The application flow:
1. User sends a message through Telegram
2. Telegram forwards the message to the AWS Lambda endpoint
3. The Lambda function processes the message using LLMs
4. A tailored response is generated and sent back to the user

## 🔮 Future Plans

- Voice message support
- Personalized health insights based on user data
- Multi-language support

## 🔒 Privacy

The AI Health Agent prioritizes user privacy. While the agent needs to remember the context of the conversation to be helpful, no health data is permanently stored or shared with third parties.

## 📄 License

[MIT License](LICENSE)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/rahul2-byte/AI-health-Assistant/issues).

---

Made with ❤️ for better health
