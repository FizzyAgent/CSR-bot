from datetime import datetime

import openai as openai

from models.messages import Message, Role

__system_messages = Message(
    role=Role.system,
    text=(
        "You are a customer service rep using an application unix-based command-line interface "
        "to interact with both customers and company resources. "
        "Your job is to help a company answer customer enquires. "
        "Follow the instructions provided in order to use the interface correctly. "
    )
)


def get_chat_input(messages: list[Message]) -> list[dict[str, str]]:
    return [m.to_gpt_message() for m in messages]


def get_chat_response(messages: list[Message], company: str, location: str) -> str:
    prompt_message = Message(
        role=Role.app,
        text=f"""The customer is connecting from {location}. Today's date is {datetime.now().strftime("%d %b %Y")}.
The company you are representing is {company}""",
    )
    messages = [__system_messages, prompt_message] + messages
    chat_input = get_chat_input(messages=messages)
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=chat_input,
    )
    return res["choices"][0]["text"]
