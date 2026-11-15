from psycopg_pool import ConnectionPool

DATABASE_URL = "postgresql://postgres:Password4242@localhost:5432/TaskFlow"

pool = ConnectionPool(
    conninfo=DATABASE_URL,
    min_size=1,
    max_size=10,
    open=False
)