from psycopg.rows import dict_row
from src.data.database import pool
from src.models.Users import Users,UserLogin,userResponse
from pwdlib import PasswordHash
from psycopg.errors import UniqueViolation

def register(user:Users):
    password_hash = PasswordHash.recommended()
    hashed_password = password_hash.hash(user.password)

    if(user.username == "" or user.password == "" ):
        return None
    
    
    try: 
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
                    
                    if row is None:
                            return None
                    
                    created_user = userResponse(
                                username=row[0],
                                email=row[1],
                                full_name=row[2],
                            )
                                    
                    return created_user
    except UniqueViolation as e:
        if e.diag.constraint_name == "users_email_unique":
            return {"error": "email"}

        elif e.diag.constraint_name == "users_username_unique":
            return {"error": "username"}
      
        raise


def login (user: UserLogin):
    password_hash = PasswordHash.recommended()
    
    with pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id,password_hasshed from users
                        where username = %s
                        """,
                        (user.username,)
                    )
                    row = cursor.fetchone()
                    if row is None:
                        return None
                    
                    actual_password = row[1]
                    
                    if password_hash.verify(user.password, actual_password):
                        return row[0]
                    
                    return None


def checkDbHealth():
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM health")

            status = cur.fetchall()

            return status
        
def getUserById(user_id):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id,username,email,full_name,is_active,created_at FROM users where id = %s",(user_id,))

            row = cur.fetchone()
            if row is None:
                return None
            return row
        
def getUserByUsername(username):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id,username,email,full_name,is_active,created_at FROM users where username = %s",(username,))

            row = cur.fetchone()
            if row is None:
                return None
            return row