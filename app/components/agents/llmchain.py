import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "python")))

from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from components.client import llm
from langchain.chains import LLMChain, SequentialChain
import yaml

# 🤖 First node gets the data from the LLM for the given prompt
def research(prompt):

    research_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(prompt),

        HumanMessagePromptTemplate.from_template('''Provide a direct, well-informed response using your medical knowledge. 
        Question: {text}'''),
        ]
    )
    
    return LLMChain(llm=llm(), prompt=research_prompt, output_key="research")



#----------------------New Node -----------------------------------#
# 🤖 Node 2 validates all the responses of Node 1
def validator(prompt):

    validation_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(prompt),

        AIMessagePromptTemplate.from_template(''' 
        Review it carefully. If the this is accurate, pass it along unchanged. If there are any errors or missing details, correct them.
        Text: {research}'''),
        ]
    )
    
    return LLMChain(llm=llm(), prompt=validation_prompt, output_key="validation")


#----------------------New Node -----------------------------------#

def output(prompt):
        
    # 🤖 Worker 3 validates all the responses of woker 1

    formating_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(prompt),

        AIMessagePromptTemplate.from_template(''' 
        Rephrase it for a general audience. Make sure the information is presented in plain language and formatted clearly.
        Text: {validation} '''),
        ]
    )

    return LLMChain(llm=llm(), prompt=formating_prompt, output_key="final_output")

def get_output(prompt):
    
    with open("app/components/agents/agent-prompts.yml", "r", encoding="utf-8") as file:
        agent_prompts = yaml.safe_load(file)
        # Return the bot commands
        prompts = {key: value for key, value in agent_prompts["prompts"].items()}

    research_chain = research(prompts["research-prompt"])

    validation_chain = validator(prompts["validation-prompt"])

    output_chain = output(prompts["output-prompt"])

    # ✅ Create SequentialChain (Pass Output from One to Another)
    seq_chain = SequentialChain(
        chains=[research_chain, validation_chain, output_chain],
        input_variables=["text"],
        output_variables=["final_output"],
        verbose=True  # ✅ Enable detailed logging
    )

    # ✅ Run the Chain
    return  seq_chain.run({ "text": prompt })