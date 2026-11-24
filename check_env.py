# check_env.py (put in the project root, run it, then delete it)
import os
from dotenv import find_dotenv, load_dotenv

print("Found .env at:", find_dotenv() or "NOT FOUND")
load_dotenv()
key = os.getenv("ANTHROPIC_API_KEY")
print("Key loaded:", bool(key), "| starts with sk-ant:", bool(key and key.startswith("sk-ant")))