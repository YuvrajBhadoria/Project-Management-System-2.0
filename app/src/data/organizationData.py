from psycopg.rows import dict_row
from src.data.database import pool
from src.models.Organization import Organization
from slugify import slugify
from .userData import getUserById
        
def createOrganization(org: Organization,user_ID):
    slug = slugify(org.name)
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO organizations (name, slug, created_by)
                VALUES (%s, %s, %s)
                RETURNING id
                """,
                (org.name, slug, user_ID)
            )

            org_id = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO organization_members
                (organization_id, user_id, role)
                VALUES (%s, %s, %s)
                """,
                (org_id, user_ID, "owner")
            )

            return org_id
            
def getUserOrganization(user_ID):
    with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                                                        """
                                                        SELECT organization_id from organization_members
                                                        where user_id = %s
                                                        """,
                                                        (user_ID,)
                                                    )
                org_ids = cursor.fetchall()
                rows = []
                for org_id in org_ids:
                    cursor.execute(
                                            """
                                            SELECT name from organizations
                                            where id = %s
                                            """,
                                            (org_id[0],)
                                        )
                    result = cursor.fetchone()
                    rows.append({
                        "name": result[0]
                    })
                                    
                if not rows:
                    return None
                
                return rows
            
def getOrganization(slug):
    with pool.connection() as conn:
                with conn.cursor(row_factory=dict_row) as cursor:
                    cursor.execute(
                                            """
                                            SELECT * from organizations
                                            where slug = %s
                                            """,
                                            (slug,)
                                        )
                    rows = cursor.fetchone()
                    
                    if rows is None:
                        return None
                    
                    rows["created_by"] = getUserById(rows["created_by"])[1]
                    return rows
                
def updateOrganization(slug: str, update_data: str):
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT * FROM organizations
                WHERE slug = %s
                """,
                (slug,)
            )

            rows = cursor.fetchone()

            if rows is None:
                return None
            
            new_slug = slugify(update_data)
            
            cursor.execute(
                """
                UPDATE organizations
                SET name = %s,slug = %s
                WHERE slug = %s
                RETURNING *
                """,
                (update_data, new_slug,slug)
            )

            updated_org = cursor.fetchone()

            return updated_org
        
  
def addOrganizationMember(org_id, user_id, role):
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                INSERT INTO organization_members
                (organization_id, user_id, role)
                VALUES (%s, %s, %s)
                RETURNING *
                """,
                (org_id, user_id, role)
            )

            return cursor.fetchone()
        
def getOrganizationMember(org_id, user_id):
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT * FROM organization_members
                WHERE organization_id = %s AND user_id = %s
                """,
                (org_id, user_id)
            )

            return cursor.fetchone()

def getOrganizationMembers(org_id):
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(
                """
                SELECT * FROM organization_members
                WHERE organization_id = %s
                """,
                (org_id,)
            )

            rows = cursor.fetchall()
            
            result = []
            for row in rows:
                username = getUserById(row["user_id"])[1]
                
                result.append({
                    "username": username,
                    "role": row["role"]
                })

                
            return result
        
def removeOrganizationMember(org_id, user_id):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            
            cursor.execute(
                """
                DELETE FROM team_members tm
                USING teams t
                WHERE tm.team_id = t.id
                AND t.organization_id = %s
                AND tm.user_id = %s
                """,
                (org_id, user_id)
            )

            cursor.execute(
                """
                DELETE FROM organization_members
                WHERE organization_id = %s
                AND user_id = %s
                RETURNING *
                """,
                (org_id, user_id)
            )

            return cursor.fetchone()