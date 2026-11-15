from psycopg.rows import dict_row
from src.data.database import pool
from src.models.Users import Users,userResponse
from pwdlib import PasswordHash


def register(user:Users):
    password_hash = PasswordHash.recommended()
    hashed_password = password_hash.hash(user.password)

    if(user.username == "" or user.password == "" ):
        return None
    
    with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users(username,email,password_hasshed,full_name)
                    VALUES (%s,%s,%s,%s)
                    RETURNING username, email, full_name
                    """,
                    (user.username,user.email,hashed_password,user.full_name)
                )
                row = cursor.fetchone()
                
                created_user = userResponse(
                    username=row[0],
                    email=row[1],
                    full_name=row[2],
                )
                
    if created_user is None:
        return None
    return created_user
def login (user: Users):
    password_hash = PasswordHash.recommended()
    
    with pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT password_hasshed from users
                        where username = %s
                        """,
                        (user.username,)
                    )
                    row = cursor.fetchone()
                    
                    actual_password = row[0]
                    
                    if password_hash.verify(user.password, actual_password):
                        return {"message": "Login Successful"}
                    
                    return None


def checkDbHealth():
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM health")

            status = cur.fetchall()

            return status