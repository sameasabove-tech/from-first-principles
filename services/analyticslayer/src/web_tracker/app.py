from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS to handle cross-origin requests
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# SQLite setup
DB_FILE = "page_hits.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
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

def track_page_hit(session_id, ip_address, page, inserted_at):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO page_hits (page, session_id, ip_address, inserted_at)
        VALUES (?, ?, ?, ?)
    """, (page, session_id, ip_address, inserted_at))
    conn.commit()
    conn.close()

def get_client_ip():
    """Extract client IP address from request headers."""
    if "X-Forwarded-For" in request.headers:
        # If the app is behind a proxy like NGINX
        return request.headers["X-Forwarded-For"].split(",")[0]
    return request.remote_addr  # Direct IP from client request

@app.route('/track', methods=['POST'])
def track_hit():
    data = request.get_json()
    page = data.get('page', 'unknown')
    session_id = data.get('session_id', 'unknown')  # get a generated session id
    ip_address = get_client_ip() # get the client's IP address

    track_page_hit(page, session_id, ip_address, datetime.today().strftime('%Y-%m-%d %H:%M:%S')) # Track the page hit and insert into db
# print(f"Page hit recorded: {page}, Session ID: {session_id}, IP: {ip_address}")
    return jsonify({
        "message": f"Page {page} hit recorded!",
        "session_id": session_id,
        "ip": ip_address,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM page_hits")
    data = cursor.fetchall()
    conn.close()
    
    return jsonify({row[0]: row[1] for row in data})

if __name__ == "__main__":
    init_db()  # Initialize the database
    app.run(debug=True)