from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    customer = "customer"
    bot = "bot"
    system = "system"

    @property
    def humanized(self) -> str:
        if self == Role.customer:
            return "You"
        elif self == Role.bot:
            return "CSR Bot"
        elif self == Role.system:
            return "App System"
        else:
            return self


class Message(BaseModel):
    role: Role
    text: str
