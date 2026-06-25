"""
Configuration loader
Developer: @rehuux | Owner: Syed Rehan
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API
API_ID = int(os.getenv('API_ID', 0))
API_HASH = os.getenv('API_HASH', '')
SESSION_STRING = os.getenv('SESSION_STRING', '')
OWNER_ID = int(os.getenv('OWNER_ID', 0))

# Settings
COOLDOWN_HOURS = int(os.getenv('COOLDOWN_HOURS', '12'))
REPLY_MESSAGE = os.getenv('REPLY_MESSAGE', 
    "Hey! My owner is currently offline right now.\n\n"
    "Feel free to leave your message, and they'll reply when they're back online."
)

# Render
PORT = int(os.getenv('PORT', 10000))
