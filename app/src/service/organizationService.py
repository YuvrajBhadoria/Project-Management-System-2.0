from src.data import organizationData as data
from src.models.Organization import Organization,OrganizationMemberCreate
from src.models.Users import UserDetail
from src.service import userService
from slugify import slugify

def createOrganization(org: Organization,user_ID):
    result = data.createOrganization(org,user_ID)
    
    if result is not None:
        
        slug = slugify(org.name)
        user:UserDetail = data.getUserById(user_ID)
        
        member = OrganizationMemberCreate(
            username = user[1],
            role = "owner"
        )
        
        addOrganizationOwner(slug,member)
    return result
    
def getUserOrganization(user_ID):
    return data.getUserOrganization(user_ID)

def getOrganization(slug):
    return data.getOrganization(slug)

def updateOrganization(slug:str ,update_data: str):
    return data.updateOrganization(slug,update_data)

def addOrganizationOwner(slug, member:OrganizationMemberCreate):
    
    user = userService.getUserByUsername(member.username)
    org = getOrganization(slug)

       
    return data.addOrganizationMember(
            org["id"],
            user[0],
            member.role
        )

def addOrganizationMember(slug, member:OrganizationMemberCreate, current_user_id):
    
    org = data.getOrganization(slug)

    if org is None:
        return {"message": "Organization Does not exists"}

 
    current_member = data.getOrganizationMember(
        org["id"],
        current_user_id
    )

    if current_member is None or current_member["role"] not in ["owner", "admin"]:
        return {"message": "You dont have permission to add a member"}
    
    
    user = userService.getUserByUsername(member.username)

    if user is None:
        return None

   
    return data.addOrganizationMember(
        org["id"],
        user[0],
        member.role
    )
    
def getOrganizationMembers(org_id,current_user_id):
    
    current_member = data.getOrganizationMember(
            org_id,
            current_user_id
        )
    
    if current_member is None or current_member["role"] not in ["owner", "admin"]:
            return {"message": "You dont have permission to view all the members"}
        
    return data.getOrganizationMembers(org_id)