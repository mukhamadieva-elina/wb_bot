from dotenv import load_dotenv
import os

load_dotenv()

# TOKEN = os.getenv("TOKEN")
TOKEN = os.getenv("TOKEN")+"/test"
bd_pass = os.getenv("bd_pass")
api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
session_str = os.getenv("session_str")
test_bd_pass = os.getenv("test_bd_pass")
api_key = os.getenv("api_key")
admin_id = 5000674828
bot_chat_name = "@xenob8bot"
telegram_client_server = "149.154.167.40"
telegram_client_port = 443
