from src.data import teamData as data
from src.models.Teams import Teams
from src.service import organizationService
from fastapi import HTTPException
from src.data import organizationData
from src.data import teamData as data

def createTeam(team: Teams,slug:str ,user_ID):
    
    org = organizationService.getOrganization(slug)

    member = organizationService.getOrganizationMember(org[0],user_ID)
    if member["role"] ==  "member":
        return {"message": "You are not eligible to create a new Team"}
    return data.createTeam(team,user_ID)

def getTeam(team_id, current_user_id):

    team = data.getTeamDetail(team_id)

    if team is None:
        raise HTTPException(404, "Team not found")

    membership = organizationData.getOrganizationMember(
        team["organization_id"],
        current_user_id
    )

    if membership is None:
        raise HTTPException(
            status_code=403,
            detail="You don't belong to this organization"
        )

    return team

def getTeamDetail(team_id):
    return data.getTeamDetail(team_id)

def updateTeam(team_id, update_data, current_user_id):

    team = getTeamDetail(team_id)

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    membership = organizationData.getOrganizationMember(
        team["organization_id"],
        current_user_id
    )

    if membership is None or membership["role"] not in ["owner", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to update this team"
        )

    return data.updateTeam(team_id, update_data)

def deleteTeam(team_id, current_user_id):

    team = data.getTeamById(team_id)

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    membership = organizationData.getOrganizationMember(
        team["organization_id"],
        current_user_id
    )

    if membership is None or membership["role"] not in ["owner", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to delete this team"
        )

    return data.deleteTeam(team_id)

def addTeamMember(team_id,user_Id):
    org = organizationService.getUserOrganization(user_Id)
    if org is None:
        raise  HTTPException(status_code=404,
                             detail="This User is not in this organization")
    
    return data.addTeamMember(team_id,user_Id)