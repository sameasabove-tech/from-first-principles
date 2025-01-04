from datetime import datetime
import sqlite3
from fastapi import Request
from fastapi.responses import JSONResponse

from config.config_utils import load_config

DB_FILE = load_config()['DATABASE']['DIR_PATH']

class WebTrackerStorage:
    def __init__(self, db_path: str):
        self.db_path = db_path

        try:
            self.init_db()
        except:
            raise RuntimeError("Error initializing database")
        
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS page_hits (
                page TEXT,
                session_id TEXT,
                ip_address TEXT,
                inserted_at TEXT,
                PRIMARY KEY (page, session_id, ip_address, inserted_at)
            )
        """)
        conn.commit()
        conn.close()

    def track_page_hit(self, session_id, ip_address, page, inserted_at):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO page_hits (page, session_id, ip_address, inserted_at)
            VALUES (?, ?, ?, ?)
        """, (page, session_id, ip_address, inserted_at))
        conn.commit()
        conn.close()

    def get_client_ip(self, request: Request):
        """Extract client IP address from request headers."""
        if "X-Forwarded-For" in request.headers:
            # If the app is behind a proxy like NGINX
            return request.headers["X-Forwarded-For"].split(",")[0]
        return request.client.host  # Direct IP from client request