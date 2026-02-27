import spotipy
import pandas as pd
import sys
import pyodbc
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
user_name = os.getenv("USER_NAME")
user_id = os.getenv("USER_ID")
server = os.getenv("SERVER")
database = os.getenv("DATABASE")
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")

connection_string = pyodbc.connect(f"Driver={{SQL Server}}; Server={server}; DATABASE={database}; UID={user}; PWD={password};")

cursor = connection_string.cursor()

scope = "user-library-read user-read-recently-played"

def check_data(song_df: pd.DataFrame) -> bool:    
    if not song_df.empty and pd.Series(song_df['played_at']).is_unique and not song_df.isnull().values.any():
        return True
    else:
        return False

try:
    token = spotipy.util.prompt_for_user_token(username=user_name, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    
    if token:
        sp = spotipy.Spotify(auth=token)
        
        try:
            user_data = sp.current_user()
            print(f"User data retrieved successfully: {user_data}")
            print(f"User display name: {user_data['display_name']}")
            print(f"User followers count: {user_data['followers']['total']}")
            print(f"User link: {user_data['external_urls']['spotify']}")            
            
            recently_played = sp.current_user_recently_played(limit=5)
            recently_played_tracks = recently_played['items']
            
            song_name = []
            artist_name = []
            played_at = []
            for track in recently_played_tracks:
                song_name.append(track['track']['name'])
                artist_name.append(track['track']['artists'][0]['name'])
                played_at.append(track['played_at'])

            song_dictionary = {
                'song_name': song_name,
                'artist_name': artist_name,
                'played_at': played_at
            }
            song_df = pd.DataFrame(song_dictionary)
            
            if check_data(song_df):                
                song_df.to_csv('recently_played_tracks.csv', index=False)
            else:            
                print("Data not validated")
                        
            
        except spotipy.exceptions.SpotifyException as e:
            print(f"Spotify API error: {e}")
        except Exception as e:
            print(f"Error retrieving user data: {e}")
    else:
        print("Failed to get token")
        
except spotipy.exceptions.SpotifyException as e:
    print(f"Spotify authentication error: {e}")
except Exception as e:
    print(f"Error during authentication: {e}")
    