import spotipy
import pandas as pd
import sys
import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print(sys.version)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
user_name = os.getenv("USER_NAME")

print(client_id, client_secret, redirect_uri, user_name)