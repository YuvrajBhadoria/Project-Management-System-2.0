from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class Teams(BaseModel):
    organization_id: UUID
    name: str
    description: str
    created_by: UUID