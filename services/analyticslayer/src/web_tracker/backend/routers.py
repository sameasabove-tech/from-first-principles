from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi import APIRouter
import sqlite3

from config.config_utils import load_config
from backend.tracking import WebTrackerStorage

DB_FILE = load_config()['DATABASE']['DIR_PATH']

WebTracker = WebTrackerStorage(DB_FILE)

router = APIRouter()

@router.get("/")
async def home_page():
    return JSONResponse({
        "message": "Welcome to the FromFirstPrincipals Web Tracker API",
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@router.post("/track")
async def track_hit(request: Request):
    data = await request.json()
    page = data.get('page', 'unknown')
    session_id = data.get('session_id', 'unknown')  # get a generated session id
    ip_address = WebTracker.get_client_ip(request)  # get the client's IP address

    WebTracker.track_page_hit(session_id, ip_address, page, datetime.today().strftime('%Y-%m-%d %H:%M:%S'))  # Track the page hit and insert into db

    return JSONResponse({
        "message": f"Page {page} hit recorded!",
        "session_id": session_id,
        "ip": ip_address,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@router.get("/stats")
async def get_stats():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM page_hits")
    data = cursor.fetchall()
    conn.close()
    
    formatted_data = [
        {
            "page": row[0],
            "session_id": row[1],
            "ip_address": row[2],
            "timestamp": row[3]
        } for row in data
    ]
    
    return JSONResponse({"data": formatted_data})


@router.get("/Community") #, response_class=HTMLResponse)
async def community_visualizer():
    """
    Returns a simple HTML response for the root endpoint.
    """
    return JSONResponse({
        "Idea 1": "Map with all people that have visited the site and their location.",
        "Idea 2": "AI Analyst: A bot that will give random insights on todays data or something dumb.",
    })