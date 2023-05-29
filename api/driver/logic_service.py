from api.driver.parser import parse_gpt_output
from api.gpt.gpt_service import get_chat_response
from app.states import save_interface_message
from api.models.messages import Message, Role
from api.models.settings import ChatSettings


def run(messages: list[Message], settings: ChatSettings, openai_key: str) -> bool:
    gpt_output = get_chat_response(
        messages=messages,
        company=settings.company,
        location=settings.location,
        resources=settings.resource_loader.get_all_resources(),
        openai_key=openai_key,
    )
    save_interface_message(
        message=Message(
            role=Role.bot,
            text=gpt_output,
        )
    )
    commands = parse_gpt_output(output=gpt_output, settings=settings)
    terminated = False
    for command in commands:
        terminated = command.run() or terminated
    return terminated
