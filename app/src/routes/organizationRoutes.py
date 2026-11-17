from fastapi import APIRouter, HTTPException, status, Depends
from src.service import userService
from pydantic import BaseModel
from ..core.dependencies import get_current_user
from src.models.Organization import  Organization,OrganizationMemberCreate
from src.service import organizationService as service


router = APIRouter()

@router.post("/organizations")
def createOrganization(org: Organization,user = Depends(get_current_user)):
    createdOrg = service.createOrganization(org,user[0])
    if createdOrg is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    return createdOrg

@router.get("/organization")
def getUserOrganization(user = Depends(get_current_user)):
    user_ID = user[0]
    userOrg = service.getUserOrganization(user_ID)
    
    if userOrg is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The User doesnt have any Organization")
    
    return userOrg

@router.get("/organization/{slug}")
def getOrganization(slug:str):
    org = service.getOrganization(slug)
    if org is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No such Organization")
    
    return org

@router.patch("/organization/{slug}")
def updateOrganization(slug:str,update_data:str):
    org = service.updateOrganization(slug,update_data)
    if org is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No such Organization")        
    return org


@router.post("/organizations/{slug}/members")
def addOrganizationMember(
    slug: str,
    member: OrganizationMemberCreate,
    current_user=Depends(get_current_user)
):
    result = service.addOrganizationMember(
        slug,
        member,
        current_user[0]
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Organization or user not found"
        )

    return result

@router.get("/organizations/{slug}/members")
def getOrganizationMembers(org_id,current_user=Depends(get_current_user)):
    return service.getOrganizationMembers(org_id,current_user[0])

@router.delete("/{slug}/members/{user_id}")
def removeOrganizationMember(
    slug: str,
    user_id,
    current_user=Depends(get_current_user)
):
    return service.removeOrganizationMember(
        slug,
        user_id,
        current_user["id"]
    )