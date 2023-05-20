from pydantic import BaseModel

from resources.resource_loader import ResourceLoader


class ChatSettings(BaseModel):
    company: str
    location: str
    resource_loader: ResourceLoader
