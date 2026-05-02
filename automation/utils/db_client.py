import sqlite3
from pathlib import Path


class DBClient:
    def __init__(self):
        project_root = Path(__file__).resolve().parents[2]
        self.db_path = project_root / "backend" / "smarthome.db"

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_device_by_id(self, device_id):
        conn = self.get_connection()
        row = conn.execute(
            "SELECT * FROM devices WHERE id = ?",
            (device_id,)
        ).fetchone()
        conn.close()

        if row is None:
            return None

        return dict(row)

    def get_latest_audit_log_by_device(self, device_id):
        conn = self.get_connection()
        row = conn.execute(
            """
            SELECT * FROM audit_logs
            WHERE device_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (device_id,)
        ).fetchone()
        conn.close()

        if row is None:
            return None

        return dict(row)