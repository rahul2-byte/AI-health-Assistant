from components.agents import llmchain

def main():

    prompt = "How many grams of protien does chiken have..?"
    output = llmchain.get_output(prompt)

    print("Final Output :- ", output)

if __name__ == "__main__":
    main()