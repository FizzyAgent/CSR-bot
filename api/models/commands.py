import random
import re
import shlex
from abc import ABC
from re import Pattern

from api.gpt.util import SAFETY_TEXT, END_MESSAGE
from app.states import save_bot_message, save_interface_message
from api.models.messages import Message, Role
from api.models.program_loader import ProgramArgParser, ProgramArgParserError
from api.models.settings import ChatSettings


class Command(ABC):
    _pattern = ...

    def __init__(self, matches: tuple[str, ...], settings: ChatSettings):
        ...

    @classmethod
    def get_regex_pattern(cls) -> Pattern[str]:
        return cls._pattern

    def run(self) -> bool:
        ...


class CoTCommand(Command):
    _pattern = re.compile(r"^chain of thoughts:", re.MULTILINE | re.IGNORECASE)

    def run(self) -> bool:
        output = "Internal chain of thoughts noted. Please continue."
        message = Message(
            role=Role.app,
            text=output,
        )
        save_interface_message(message=message)
        return False


class EchoCommand(Command):
    _pattern = re.compile(r'echo \$ "((?:.|\s)*)"\s+.*evaluation: (\w*)', re.MULTILINE)

    def __init__(self, matches: tuple[str, ...], settings: ChatSettings):
        assert len(matches) == 2
        super().__init__(matches=matches, settings=settings)
        self.text = matches[0]
        self.safety = matches[1]

    def run(self) -> bool:
        output = self.text if self.safety == "safe" else SAFETY_TEXT
        bot_message = Message(
            role=Role.bot,
            text=output,
        )
        save_bot_message(message=bot_message)
        return False


class ErrorCommand(Command):
    def run(self) -> bool:
        error_message = Message(
            role=Role.app,
            text="Unknown command, did you use the correct syntax?",
        )
        save_interface_message(message=error_message)
        return False


class ResourceCommand(Command):
    _pattern = re.compile(r"cat (.*)")

    def __init__(self, matches: tuple[str, ...], settings: ChatSettings):
        assert len(matches) == 1
        super().__init__(matches=matches, settings=settings)
        self.file_name = matches[0]
        self.resource_loader = settings.resource_loader

    def run(self) -> bool:
        resource = self.resource_loader.load_resource(file_name=self.file_name)
        resource_message = Message(
            role=Role.app,
            text=resource,
        )
        save_interface_message(message=resource_message)
        return False


class ProgramInfoCommand(Command):
    _pattern = re.compile(r"python (.*).py.*--help.*")

    def __init__(self, matches: tuple[str, ...], settings: ChatSettings):
        assert len(matches) == 1
        super().__init__(matches=matches, settings=settings)
        self.file_name = matches[0]
        self.program_loader = settings.program_loader

    def run(self) -> bool:
        try:
            program = self.program_loader.load_program(file_name=self.file_name)
        except:
            error_message = Message(
                role=Role.app,
                text="Program not found: {}\nDid you check available resources for the correct program?".format(
                    self.file_name
                ),
            )
            save_interface_message(message=error_message)
            return False
        program_message = Message(
            role=Role.app,
            text=program.help,
        )
        save_interface_message(message=program_message)
        return False


class ProgramRunCommand(Command):
    _pattern = re.compile(r"python (.*).py ?((?!--help).+)?$")

    def __init__(self, matches: tuple[str, ...], settings: ChatSettings):
        assert len(matches) == 2
        super().__init__(matches=matches, settings=settings)
        self.file_name = matches[0]
        self.args = matches[1] or ""
        self.program_loader = settings.program_loader

    def run(self) -> bool:
        try:
            program = self.program_loader.load_program(file_name=self.file_name)
        except:
            error_message = Message(
                role=Role.app,
                text=(
                    f"Program not found: {self.file_name}\n"
                    "Did you check available resources for the correct program?"
                ),
            )
            save_interface_message(message=error_message)
            return False
        arg_parser = ProgramArgParser()
        for arg in program.args:
            arg_parser.add_argument("--" + arg, required=True)
        for arg in program.optional_args:
            arg_parser.add_argument("--" + arg)
        try:
            _ = arg_parser.parse_args(shlex.split(self.args))
            output = (
                program.success_message
                if len(program.possible_errors) == 0 or random.random() > 0.2
                else random.choice(program.possible_errors)
            )
        except ProgramArgParserError as e:
            output = str(e)
        program_message = Message(
            role=Role.app,
            text=output,
        )
        save_interface_message(message=program_message)
        return False


class ExitCommand(Command):
    _pattern = re.compile(r"exit\(\)")

    def run(self) -> bool:
        save_bot_message(message=END_MESSAGE)
        return True
