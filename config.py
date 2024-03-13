from dotenv import load_dotenv
import os

load_dotenv()


TOKEN=os.getenv("TOKEN")
bd_pass=os.getenv("bd_pass")
api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
session_str = os.getenv("session_str")

api_key = os.getenv("api_key")