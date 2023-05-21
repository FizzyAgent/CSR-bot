from pydantic import BaseModel

from api.models.program_loader import ProgramLoader
from api.models.resource_loader import ResourceLoader


class ChatSettings(BaseModel):
    company: str
    location: str
    resource_loader: ResourceLoader
    program_loader: ProgramLoader
