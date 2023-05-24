from enum import Enum

from pydantic import BaseModel


class Role(str, Enum):
    customer = "customer"
    bot = "bot"
    system = "system"
    app = "app"

    @property
    def humanized(self) -> str:
        if self == Role.customer:
            return "You"
        elif self == Role.bot:
            return "CSR Bot"
        elif self == Role.system:
            return "System"
        elif self == Role.app:
            return "Interface App"
        else:
            return self

    @property
    def gpt_format(self) -> str:
        if self == Role.bot:
            return "assistant"
        elif self == Role.system:
            return "system"
        elif self == Role.app:
            return "user"
        else:
            raise Exception(f"Role {self} is not supported by GPT-4")


class Message(BaseModel):
    role: Role
    text: str

    def to_gpt_message(self) -> dict[str, str]:
        return {
            "role": self.role.gpt_format,
            "content": self.text,
        }
