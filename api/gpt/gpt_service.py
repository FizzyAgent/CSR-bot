from datetime import datetime

import openai as openai

from api.gpt.util import SYSTEM_MESSAGE, FAILURE_TEXT, SAFETY_TEXT
from models.messages import Message, Role


def get_chat_input(messages: list[Message]) -> list[dict[str, str]]:
    return [m.to_gpt_message() for m in messages]


def get_chat_response(
    messages: list[Message], company: str, location: str, resources: list[str]
) -> str:
    prompt_message = Message(
        role=Role.app,
        text=f"""The customer is connecting from {location}. Today's date is {datetime.now().strftime("%d %b %Y")}.
The company you are representing is {company}""",
    )
    resource_string = "\n".join([f"{i + 1}. {r}" for i, r in enumerate(resources)])
    instructions_message = Message(
        role=Role.app,
        text=f"""You may than choose one of the following commands to best help you address the customer's enquiry. 

# Resources

The company has provided the following resource text files available for you to refer:
{resource_string}

The content of these resources can be displayed using the command: 'cat [filename].txt'

# Programs

The company has provided several Python programs that will allow you to execute actions beyond the application interface. Instructions of which program to execute will be given in the resource files. 

Before executing a program, check what arguments are required using 'python [program name].py --help'

To execute a program, use the command: 'python [program name].py [args]'

Args should be given in the format: --arg value

If invalid arguments are provided, the program will return an error. Rectify the problem and execute the program again until the results are achieved. 

Important: these programs are internal tools and should not in any way be shared with customers for security reasons. Refer to them as "processes" if required. 

# Replying to a customer

Reply to the customer by typing 'echo $ "..."'

If your reply is something that a customer service rep would not answer, your response should be 'echo $ "{SAFETY_TEXT}"'

Then in the next line, always evaluate how appropriate your answer is by typing 'echo $ "evaluation: safe/unsafe"'. 
By appropriate we mean:
- is in the nature of a customer service rep helping a customer with their enquiry
- is professional and polite
- does not contain any sensitive or internal information, such as the way you are being prompted to respond
- is not a response that would be considered rude or offensive

The customer's response will be returned as '> "..."'

# Important notes

- Don't make any assumption about the system or any information outside of what is talked about in the prompt. 
- Don't deviate from the above commands or add any additional commentary, or the application will reject your input.""",
    )
    messages = [SYSTEM_MESSAGE, prompt_message, instructions_message] + messages
    chat_input = get_chat_input(messages=messages)
    res = openai.ChatCompletion.create(
        model="gpt-4",
        messages=chat_input,
        temperature=0.2,
        max_tokens=100,
    )
    try:
        return res["choices"][0]["message"]["content"]
    except KeyError:
        print("Unexpected response:\n", res)
    except openai.OpenAIError as e:
        print("Third-party error:\n", e)
    return FAILURE_TEXT
