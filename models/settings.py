from pydantic import BaseModel

from models.resource_loader import ResourceLoader


class ChatSettings(BaseModel):
    company: str
    location: str
    resource_loader: ResourceLoader
