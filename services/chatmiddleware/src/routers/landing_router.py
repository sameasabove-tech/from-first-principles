from fastapi import APIRouter
from fastapi.responses import HTMLResponse


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def read_root():
    """
    Returns a simple HTML response for the root endpoint.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LLM Chat App</title>
        <link rel="stylesheet" type="text/css" href="styles.css">
    </head>
    <body>
        <div class="container">
            <div class="chat-container" id="chat-container">
                <div class="chat-header">
                    <h2>Chat with LLM</h2>
                    <select id="llm-model">
                        <option value="gemini">Gemini</option>
                        </select>
                </div>
                <div class="chat-body">
                    <div id="chat-messages">
                        </div>
                    <div class="chat-footer">
                        <input type="text" id="chat-input" placeholder="Type your message...">
                        <button id="send-btn">Send</button>
                    </div>
                </div>
            </div>
        </div>

        <script src="script.js"></script>
    </body>
    </html>
    """
