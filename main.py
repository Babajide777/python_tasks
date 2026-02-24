import spotipy
import pandas as pd
import sys
import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# print(sys.version)

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
user_name = os.getenv("USER_NAME")
user_id = os.getenv("USER_ID")

# print(client_id, client_secret, redirect_uri, user_name, user_id)

scope = "user-library-read user-read-recently-played"

token = spotipy.util.prompt_for_user_token(username=user_name, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
    print(f"Token: {token} \n Spotify Object: {sp}")    
else:
    print("Failed to get token")
    
user_data = sp.current_user()
    