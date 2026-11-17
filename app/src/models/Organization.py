from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from typing import Literal

class Organization(BaseModel):
    name: str
    
class CreateOrganization(BaseModel):
    id: UUID
    name: str
    slug: str
    created_by: UUID
    created_at: datetime
    


class OrganizationMemberCreate(BaseModel):
    username: str
    role: Literal["admin", "member"] = "member"
    