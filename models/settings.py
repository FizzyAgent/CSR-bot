from pydantic import BaseModel


class ChatSettings(BaseModel):
    company: str
    location: str
