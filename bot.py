"""
Telegram Offline Auto-Reply Userbot
Python 3.11 compatible
Developer: @rehuux | Owner: Syed Rehan
"""

import asyncio
import time
import os
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.sessions import StringSession

# ===== CONFIGURATION =====
SESSION_STRING = os.getenv('SESSION_STRING', '')
API_ID = int(os.getenv('API_ID', 0))
API_HASH = os.getenv('API_HASH', '')
OWNER_ID = int(os.getenv('OWNER_ID', 0))
COOLDOWN_HOURS = int(os.getenv('COOLDOWN_HOURS', '12'))
REPLY_MESSAGE = os.getenv('REPLY_MESSAGE',
    "Hey! My owner is currently offline right now.\n\n"
    "Feel free to leave your message, and they'll reply when they're back online."
)
# =========================

if not SESSION_STRING:
    print("❌ SESSION_STRING not set!")
    exit(1)

print("✅ All environment variables loaded!")

# ✅ FIX: Explicitly get or create event loop
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# Create client with session string
client = TelegramClient(
    StringSession(SESSION_STRING),
    API_ID,
    API_HASH,
    loop=loop,  # ✅ Pass loop explicitly
    device_model='OfflineReplyBot',
    system_version='1.0'
)

last_reply = {}

@client.on(events.NewMessage(incoming=True))
async def handle_message(event):
    try:
        if event.out:
            return
        if event.is_group or event.is_channel:
            return
        
        sender_id = event.sender_id
        if sender_id == OWNER_ID:
            return
        
        current_time = time.time()
        if sender_id in last_reply:
            elapsed = (current_time - last_reply[sender_id]) / 3600
            if elapsed < COOLDOWN_HOURS:
                remaining = int(COOLDOWN_HOURS - elapsed)
                print(f"⏳ Cooldown: User {sender_id} — {remaining}h remaining")
                return
        
        try:
            await event.reply(REPLY_MESSAGE)
            last_reply[sender_id] = current_time
            print(f"✅ Auto-reply sent to user {sender_id}")
        except FloodWaitError as e:
            print(f"⏳ Flood wait: {e.seconds}s")
            await asyncio.sleep(e.seconds)
            
    except Exception as e:
        print(f"⚠️ Error: {e}")

@client.on(events.Disconnect)
async def on_disconnect():
    print("🔴 Disconnected from Telegram")

@client.on(events.Connected)
async def on_connect():
    print("🟢 Connected to Telegram")

async def main():
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 OFFLINE AUTO-REPLY USERBOT
👨‍💻 Developer: @rehuux
👤 Owner: Syed Rehan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Starting with session string (NO OTP)
📱 Monitoring private messages...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    try:
        await client.start()
        me = await client.get_me()
        print(f"✅ Logged in as: {me.first_name} (@{me.username or 'no username'})")
        print(f"👤 Owner ID: {OWNER_ID}")
        print(f"🕐 Cooldown: {COOLDOWN_HOURS} hours")
        print("\n🟢 Bot is running! Listening for messages...\n")
        
        await client.run_until_disconnected()
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
