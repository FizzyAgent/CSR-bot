from models.commands import Command
from models.settings import ChatSettings


def parse_gpt_output(output: str, settings: ChatSettings) -> list[Command]:
    for l in output.splitlines():
        ...
