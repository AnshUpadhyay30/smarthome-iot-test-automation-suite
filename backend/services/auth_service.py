from database import get_db_connection


def login_user(email, password):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (email, password)
    ).fetchone()
    conn.close()

    if user is None:
        return None

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "token": f"mock-token-{user['id']}"
    }


def validate_token(token):
    if not token:
        return None

    if not token.startswith("mock-token-"):
        return None

    try:
        user_id = int(token.replace("mock-token-", ""))
    except ValueError:
        return None

    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()
    conn.close()

    if user is None:
        return None

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"]
    }