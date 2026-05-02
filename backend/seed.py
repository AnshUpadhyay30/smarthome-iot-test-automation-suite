from database import get_db_connection, init_db


def seed_data():
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM audit_logs")
    cursor.execute("DELETE FROM devices")
    cursor.execute("DELETE FROM users")

    cursor.execute("""
        INSERT INTO users (id, name, email, password, role)
        VALUES (?, ?, ?, ?, ?)
    """, (1, "Ansh QA", "admin@test.com", "admin123", "ADMIN"))

    devices = [
        (
            1,
            "Living Room Smart AC",
            "AC",
            "ONLINE",
            "OFF",
            24,
            None,
            None,
            "COOL",
            None,
            None,
            "1.0.0",
            1
        ),
        (
            2,
            "Bedroom Smart TV",
            "TV",
            "ONLINE",
            "OFF",
            None,
            None,
            20,
            "HDMI",
            None,
            None,
            "1.0.1",
            1
        ),
        (
            3,
            "Kitchen Smart Refrigerator",
            "REFRIGERATOR",
            "ONLINE",
            "ON",
            4,
            -18,
            None,
            "ECO",
            None,
            None,
            "1.0.2",
            1
        ),
        (
            4,
            "Laundry Washing Machine",
            "WASHING_MACHINE",
            "ONLINE",
            "OFF",
            None,
            None,
            None,
            "NORMAL",
            "IDLE",
            3,
            "1.0.0",
            1
        )
    ]

    cursor.executemany("""
        INSERT INTO devices (
            id, name, type, status, power, temperature,
            freezer_temperature, volume, mode, cycle_status,
            water_level, firmware_version, owner_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, devices)

    conn.commit()
    conn.close()
    print("Database initialized and seed data inserted.")


if __name__ == "__main__":
    seed_data()