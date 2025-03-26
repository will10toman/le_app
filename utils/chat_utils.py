import re
import hashlib
from html import escape

def parse_message(msg):
    msg = re.sub(r'(https?://\S+)', r'<a href="\1" target="_blank">\1</a>', msg)
    return escape(msg).replace("\n", "<br>")

def get_user_color(username):
    hex_color = hashlib.md5(username.encode()).hexdigest()[:6]
    return f"#{hex_color}"

def get_msg_id(user, timestamp, i):
    return f"{user}_{timestamp}_{i}"
