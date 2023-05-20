import random
import re
import shlex
from abc import ABC
from re import Pattern

from api.gpt.util import SAFETY_TEXT
from app.states import save_bot_message, save_interface_message
from models.messages import Message, Role
from models.program_loader import ProgramArgParser, ProgramArgParserError
from models.settings import ChatSettings


class Command(ABC):
    _pattern = ...

    def __init__(self, matches: tuple[str, ...], settings: ChatSettings):
        ...

    @classmethod
    def get_regex_pattern(cls) -> Pattern[str]:
        return cls._pattern

    def run(self):
        ...


class EchoCommand(Command):
    _pattern = re.compile(r'echo \$ "(.*)"\s+.*evaluation: (\w*)', re.MULTILINE)

    def __init__(self, matches: tuple[str, ...], settings: ChatSettings):
        assert len(matches) == 2
        super().__init__(matches=matches, settings=settings)
        self.text = matches[0]
        self.safety = matches[1]

    def run(self):
        output = self.text if self.safety == "safe" else SAFETY_TEXT
        bot_message = Message(
            role=Role.bot,
            text=output,
        )
        save_bot_message(message=bot_message)


class SafeEchoCommand(EchoCommand):
    def __init__(self, matches: tuple[str, ...], settings: ChatSettings):
        super().__init__(matches=(SAFETY_TEXT, "safe"), settings=settings)


class ResourceCommand(Command):
    _pattern = re.compile(r"cat (.*)")

    def __init__(self, matches: tuple[str, ...], settings: ChatSettings):
        assert len(matches) == 1
        super().__init__(matches=matches, settings=settings)
        self.file_name = matches[0]
        self.resource_loader = settings.resource_loader

    def run(self):
        resource = self.resource_loader.load_resource(file_name=self.file_name)
        resource_message = Message(
            role=Role.app,
            text=resource,
        )
        save_interface_message(message=resource_message)


class ProgramInfoCommand(Command):
    _pattern = re.compile(r"python (.*).py --help")

    def __init__(self, matches: tuple[str, ...], settings: ChatSettings):
        assert len(matches) == 1
        super().__init__(matches=matches, settings=settings)
        self.file_name = matches[0]
        self.program_loader = settings.program_loader

    def run(self):
        program = self.program_loader.load_program(file_name=self.file_name)
        program_message = Message(
            role=Role.app,
            text=program.help,
        )
        save_interface_message(message=program_message)


class ProgramRunCommand(Command):
    _pattern = re.compile(r"python (.*).py (.*)$")

    def __init__(self, matches: tuple[str, ...], settings: ChatSettings):
        assert len(matches) == 2
        super().__init__(matches=matches, settings=settings)
        self.file_name = matches[0]
        self.args = matches[1]
        self.program_loader = settings.program_loader

    def run(self):
        program = self.program_loader.load_program(file_name=self.file_name)
        arg_parser = ProgramArgParser()
        for arg in program.args:
            arg_parser.add_argument("--" + arg)
        try:
            _ = arg_parser.parse_args(shlex.split(self.args))
            output = (
                program.success_message
                if random.random() > 0.1
                else random.choice(program.possible_errors)
            )
        except ProgramArgParserError as e:
            output = str(e)
        program_message = Message(
            role=Role.app,
            text=output,
        )
        save_interface_message(message=program_message)
