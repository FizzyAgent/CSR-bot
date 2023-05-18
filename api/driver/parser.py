import re
from typing import Type

from models.commands import Command, EchoCommand
from models.settings import ChatSettings

__all_commands: list[Type[Command]] = [
    EchoCommand,
]


def parse_gpt_output(output: str, settings: ChatSettings) -> list[Command]:
    parsed_commands: list[Command] = []
    for command in __all_commands:
        if match := re.search(command.get_regex_pattern(), output):
            parsed_commands.append(command(match=match, settings=settings))
