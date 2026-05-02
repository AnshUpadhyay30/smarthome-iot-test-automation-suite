from database import get_db_connection


def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]
    return column_name in columns


def migrate():
    conn = get_db_connection()
    cursor = conn.cursor()

    if not column_exists(cursor, "devices", "health_status"):
        cursor.execute("ALTER TABLE devices ADD COLUMN health_status TEXT DEFAULT 'HEALTHY'")

    if not column_exists(cursor, "devices", "error_code"):
        cursor.execute("ALTER TABLE devices ADD COLUMN error_code TEXT")

    if not column_exists(cursor, "devices", "wifi_signal"):
        cursor.execute("ALTER TABLE devices ADD COLUMN wifi_signal TEXT DEFAULT 'GOOD'")

    conn.commit()
    conn.close()

    print("✅ Health columns migration completed.")


if __name__ == "__main__":
    migrate()