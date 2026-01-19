from backend.db import get_conn

def login(username, password):
    """
    Authenticate user and return role.
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            # Parameterized query to prevent SQL injection
            cur.execute(
                "SELECT role FROM users WHERE username=%s AND password=%s",
                (username, password)
            )
            r = cur.fetchone()
    finally:
        conn.close()

    return r[0] if r else None
