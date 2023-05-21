from api.driver.parser import parse_gpt_output
from api.gpt.gpt_service import get_chat_response
from app.states import save_interface_message
from api.models.messages import Message, Role
from api.models.settings import ChatSettings


def run(messages: list[Message], settings: ChatSettings):
    gpt_output = get_chat_response(
        messages=messages,
        company=settings.company,
        location=settings.location,
        resources=settings.resource_loader.get_all_resources(),
    )
    save_interface_message(
        message=Message(
            role=Role.bot,
            text=gpt_output,
        )
    )
    commands = parse_gpt_output(output=gpt_output, settings=settings)
    for command in commands:
        command.run()
