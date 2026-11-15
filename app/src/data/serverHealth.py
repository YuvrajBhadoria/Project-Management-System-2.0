from psycopg.rows import dict_row
from data.database import pool


def checkDbHealth():
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM health")

            status = cur.fetchall()

            return status