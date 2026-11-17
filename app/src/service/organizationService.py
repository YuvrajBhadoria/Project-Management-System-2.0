from src.data import organizationData as data
from src.models.Organization import Organization,OrganizationMemberCreate
from src.models.Users import UserDetail
from src.service import userService
from slugify import slugify

def createOrganization(org: Organization,user_ID):
    return data.createOrganization(org,user_ID)
    
def getUserOrganization(user_ID):
    return data.getUserOrganization(user_ID)

def getOrganization(slug):
    return data.getOrganization(slug)

def updateOrganization(slug:str ,update_data: str):
    return data.updateOrganization(slug,update_data)


def addOrganizationMember(slug, member:OrganizationMemberCreate, current_user_id):
    
    org = data.getOrganization(slug)

    if org is None:
        return {"message": "Organization Does not exists"}

 
    current_member = getOrganizationMember(
        org["id"],
        current_user_id
    )

    if current_member is None or current_member["role"] not in ["owner", "admin"]:
        return {"message": "You dont have permission to add a member"}
    
    
    user = userService.getUserByUsername(member.username)

    if user is None:
        return None

    if current_member["role"] == "admin" and member.role == "owner":
        return {"message": "You dont have permission to make another Owner"}
        
    return data.addOrganizationMember(
        org["id"],
        user[0],
        member.role
    )
    
def getOrganizationMembers(org_id,current_user_id):
    
    current_member = getOrganizationMember(
            org_id,
            current_user_id
        )
    
    if current_member is None or current_member["role"] not in ["owner", "admin"]:
            return {"message": "You dont have permission to view all the members"}
        
    return data.getOrganizationMembers(org_id)

def getOrganizationMember(org_id, user_id):
    return data.getOrganizationMember(org_id,user_id)

from fastapi import HTTPException

def removeOrganizationMember(slug, user_id, current_user_id):

    org = data.getOrganization(slug)

    if org is None:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )

    current_member = data.getOrganizationMember(
        org["id"],
        current_user_id
    )

    if current_member is None:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this organization"
        )

    if current_member["role"] not in ["owner", "admin"]:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to remove members"
        )

    target_member = data.getOrganizationMember(
        org["id"],
        user_id
    )

    if target_member is None:
        raise HTTPException(
            status_code=404,
            detail="User is not a member of this organization"
        )

    if target_member["role"] == "owner":
        raise HTTPException(
            status_code=403,
            detail="Organization owner cannot be removed"
        )

    if current_member["role"] == "admin" and target_member["role"] == "admin":
        raise HTTPException(
            status_code=403,
            detail="Admins cannot remove other admins"
        )

    result = data.removeOrganizationMember(
        org["id"],
        user_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Membership not found"
        )

    return {"message": "Member removed successfully"}