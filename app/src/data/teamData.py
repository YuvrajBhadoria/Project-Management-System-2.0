from psycopg.rows import dict_row
from src.data.database import pool
from .userData import getUserById
from src.models.Teams import Teams


def createTeam(team: Teams,user_ID):
    created_by = getUserById(user_ID)
    with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                     """
                     INSERT INTO teams (organization_id,name,description,created_by)
                     VALUES (%s, %s,%s, %s)
                     RETURNING id
                     """,
                     (team.organization_id,team.name,team.description,created_by[1])
                 )
                result = cursor.fetchone()
                return result
                
                
def getTeams(org_id):
    with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                     """
                     select * from teams where organization_id = %s
                     """,
                     (org_id)
                 )
                result = cursor.fetchone()
                return result
                
                
def getTeamDetail(team_id):
    with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                     """
                     select * from teams where id = %s
                     """,
                     (team_id)
                 )
                result = cursor.fetchone()
                return result

def updateTeam(team_id, update_data: dict):
    with pool.connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT * FROM teams
                WHERE id = %s
                """,
                (team_id,)
            )

            team = cursor.fetchone()

            if team is None:
                return None

            name = update_data.get("name", team["name"])
            description = update_data.get("description", team["description"])

            cursor.execute(
                """
                UPDATE teams
                SET name = %s,
                    description = %s
                WHERE id = %s
                RETURNING *
                """,
                (name, description, team_id)
            )

            return cursor.fetchone()

def deleteTeam(team_id):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM teams
                WHERE id = %s
                RETURNING *
                """,
                (team_id,)
            )

            return cursor.fetchone()