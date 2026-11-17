from fastapi import APIRouter, HTTPException, status, Depends
from src.service import teamService as service
from pydantic import BaseModel
from ..core.dependencies import get_current_user
from src.models.Teams import  Teams

router = APIRouter()

from pydantic import BaseModel, Field

class TeamUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = None


@router.post("/organizations/{slug}/teams")
def createTeam(team: Teams,
               slug: str,
               user = Depends(get_current_user)
               ):
    result = service.createTeam(team,slug,user[0])
    
    return result

@router.get("/organizations/{slug}/teams")
def getTeams(slug: str):
    result = service.getTeams(slug)
    
    
    return result

@router.get("/teams/{team_id}")
def getTeamDetail(team_id):
    result = service.getTeamDetail(team_id)
    
    return result

@router.patch("/teams/{team_id}")
def updateTeam(
    team_id,
    team: TeamUpdate,
    current_user=Depends(get_current_user)
):
    update_data = team.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided for update"
        )

    return service.updateTeam(
        team_id,
        update_data,
        current_user["id"]
    )
    
@router.delete("/teams/{team_id}")
def deleteTeam(
    team_id,
    current_user=Depends(get_current_user)
):
    return service.deleteTeam(
        team_id,
        current_user["id"]
    )
    
@router.post("/teams/{team_id}/members")
def addTeamMember(team_id,user = Depends(get_current_user)):
    result = service.addTeamMember(team_id,user[0])
    return result