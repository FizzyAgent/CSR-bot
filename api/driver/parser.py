from typing import Type

from api.models.commands import (
    Command,
    EchoCommand,
    ErrorCommand,
    ResourceCommand,
    ProgramInfoCommand,
    ProgramRunCommand,
    ExitCommand,
)
from api.models.settings import ChatSettings

__all_commands: list[Type[Command]] = [
    ResourceCommand,
    ProgramInfoCommand,
    ProgramRunCommand,
    EchoCommand,
    ExitCommand,
]


def parse_gpt_output(output: str, settings: ChatSettings) -> list[Command]:
    parsed_commands: list[Command] = []
    for command in __all_commands:
        if match := command.get_regex_pattern().search(output):
            parsed_commands.append(command(matches=match.groups(), settings=settings))
    if len(parsed_commands) == 0:
        parsed_commands.append(ErrorCommand(matches=(), settings=settings))
    return parsed_commands
