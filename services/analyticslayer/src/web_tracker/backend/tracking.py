from datetime import datetime
import sqlite3
from fastapi import Request
from fastapi.responses import JSONResponse
import logging

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
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create or update the table schema
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        ip_address TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        page TEXT NOT NULL,
                        referrer TEXT,  -- New column for referring page
                        inserted_at DATETIME NOT NULL
                    )
                """)
                
                # Create indexes for faster lookups
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_event_session ON events (session_id);
                """)
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_event_time ON events (inserted_at);
                """)
                
                conn.commit()
        except Exception as e:
            logging.error(f"Error initializing the database: {e}")
            raise

    def track_event(self, session_id, ip_address, event_type, page, referrer, inserted_at):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO events (session_id, ip_address, event_type, page, referrer, inserted_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (session_id, ip_address, event_type, page, referrer, inserted_at))
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Error tracking event: {e}")
            raise

    def get_client_ip(self, request: Request):
        """Extract client IP address from request headers."""
        if "X-Forwarded-For" in request.headers:
            # If the app is behind a proxy like NGINX
            return request.headers["X-Forwarded-For"].split(",")[0]
        return request.client.host  # Direct IP from client request