import os
import psycopg2

DB_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:postgreSQLn%40nrony0911@localhost:5432/resume_parser_DB")


def get_conn():
    """Return a new psycopg2 connection using DATABASE_URL."""
    return psycopg2.connect(DB_URL)


def init_db():
    """Initialize the database by executing statements in schema.sql.

    This is a lightweight initializer intended for development. It splits
    the SQL file on semicolons and executes non-empty statements. For
    production migrations use a real migration tool (alembic, flyway, etc.).
    """
    base = os.path.dirname(__file__)
    schema_path = os.path.join(base, "schema.sql")
    if not os.path.exists(schema_path):
        return
    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()

    # Execute each statement separately
    conn = get_conn()
    try:
        cur = conn.cursor()
        for stmt in sql.split(";"):
            s = stmt.strip()
            if not s:
                continue
            cur.execute(s)
        conn.commit()
        cur.close()
    finally:
        conn.close()
