import os
import sys
import warnings
import threading

from dotenv import load_dotenv

import panel as pn

from crew import HelloWorld
from crew import chat_interface

from crewai.agents.agent_builder.base_agent_executor_mixin import CrewAgentExecutorMixin
import time


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

load_dotenv()

pn.extension(design="material")


def custom_ask_human_input(self, final_answer: dict) -> str:
    global user_input

    chat_interface.send(final_answer, user="Assistant", respond=False)
    prompt = "Please provide feedback on the final Result:"
    chat_interface.send(prompt, user="System", respond=False)

    while user_input == None:
        time.sleep(1)

    human_comments = user_input
    user_input = None

    return human_comments


CrewAgentExecutorMixin._ask_human_input = custom_ask_human_input

user_input = None
crew_started = False


def initiate_chat(message):
    global crew_started
    crew_started = True

    try:
        inputs = {'city': message}
        crew = HelloWorld().crew()
        result = crew.kickoff(inputs=inputs)

    except Exception as e:
        chat_interface.send(f"An error occurred while running the crew: {e}", user="Assistant", respond=False)

    crew_started = False


def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    global crew_started
    global user_input

    if not crew_started:
        thread = threading.Thread(target=initiate_chat, args=(contents,))
        thread.start()

    else:
        user_input = contents


chat_interface.callback = callback

chat_interface.send(
    "Welcome! Please enter the city for the weather report",
    user="Assistant",
    respond=False
)

chat_interface.servable()
