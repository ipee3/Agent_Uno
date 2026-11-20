import os
import asyncio

from dotenv import load_dotenv #from file import something
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential
import streamlit as st


load_dotenv()  # take environment variables from .env.

async def main ():

    #get endpoint and model from .env
    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT") 
    model = os.getenv("FOUNDRY_MODEL")

    if not endpoint or not model:
        raise ValueError("Endpoint or model missing from .env")

    #initialize FoundryChatClient with AzureCliCredential
    client = FoundryChatClient(
                project_endpoint=endpoint,
                model=model,
                credential=AzureCliCredential(),
            )

    #initialize Agent
    agent = Agent(
        client=client,
        name="Agent Uno",
        description="A simple agent that answers to general questions",
        instructions=" You are a helpful assistant that answers to general questions. You can answer questions about any topic but keep it very simple.",
    )

    #print("Agent Uno is Ready to answer, put q to quit")
    #while True:
        #question = input("You: ")
        #if question.lower() == "q":
         #       print("Exiting...")
          #      break
        #
        #response = await agent.run(question)     
        #print()
        #print("Agent Uno: " + response.text)
    st.title("Agent Uno")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Näytetään keskusteluhistoria
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Viestikenttä
    if question := st.chat_input("Kirjoita viesti..."):

        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.write(question)

        response = await agent.run(question)

        with st.chat_message("assistant"):
            st.write(response.text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response.text}
        )

       

    
if __name__ == "__main__":
    asyncio.run(main())