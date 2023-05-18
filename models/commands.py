from abc import ABC
from re import Match

from app.states import save_bot_message
from models.messages import Message, Role
from models.settings import ChatSettings


class Command(ABC):

    def __init__(self, match: Match[str], settings: ChatSettings):
        ...

    @staticmethod
    def get_regex_pattern() -> str:
        ...

    def run(self):
        ...


class EchoCommand(Command):

    @staticmethod
    def get_regex_pattern() -> str:
        return r'echo $ "(.*)"\necho $ "evaluation (.*)"'

    def __init__(self, match: Match[str], settings: ChatSettings):
        assert len(match.groups()) == 2
        super().__init__(match=match, settings=settings)
        self.text = match.group(1)
        self.safety = match.group(2)

    def run(self):
        bot_message = Message(
            role=Role.bot,
            text=self.text,
        )
        save_bot_message(message=bot_message)
