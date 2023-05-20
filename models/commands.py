import re
from abc import ABC
from re import Pattern

from api.gpt.util import SAFETY_TEXT
from app.states import save_bot_message, save_interface_message
from models.messages import Message, Role
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
    _pattern = re.compile(r'cat (.*)')

    def __init__(self, matches: tuple[str, ...], settings: ChatSettings):
        assert len(matches) > 0
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
