from components.agents import llmchain
from components.messanger import Bot

def main():

    prompt = "How many grams of protien does chiken have..?"
    # output = llmchain.get_output(prompt)
    # print("Final Output :- ", output)
    
    bot = Bot()
    
    text = bot.run()

    print("Text", text)

if __name__ == "__main__":
    main()