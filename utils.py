import hashlib
from datetime import datetime

# === Get a consistent color for a username ===
def get_user_color(username):
    hex_color = hashlib.md5(username.encode()).hexdigest()[:6]
    return f"#{hex_color}"

# === Format timestamp nicely ===
def format_timestamp(ts):
    try:
        dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y %I:%M %p")
    except Exception:
        return ts  # fallback

# === Escape and format chat messages ===
def parse_message(msg):
    from html import escape
    import re
    msg = escape(msg)
    msg = re.sub(r'(https?://\S+)', r'<a href="\1" target="_blank">\1</a>', msg)
    return msg.replace("\n", "<br>")

# === Emoji Reactions helper ===
def get_reaction_count(state_reactions, msg_id, emoji):
    return state_reactions.get(msg_id, {}).get(emoji, 0)
