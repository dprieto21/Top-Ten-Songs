import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
from sqlite3 import Error
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error:
        print("Database not found.")
    return None

def get_key(key_name):
    '''
    Returns the key needed in order to access an API that's been stored in a 
    database.
    
    Args-
        key_name: Name I gave to the keys I have stored in a database.
        
    '''
    conn = create_connection("config.db")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT Key FROM api_keys WHERE Key_Name = '{}';".format(key_name))
        key = cur.fetchone()[0]
        return key

def get_artists_uri(artist_search, sp):
    '''
    Returns the URI of an artist needed to search for their content.
    
    Args-
        artist_search: The artist to search the URI for.
        sp: The variable used to be able to use methods from Spotipy.
    '''
    
    result = sp.search(artist_search, limit = 1)
    
    if result:
        for count, info in enumerate(result["tracks"]["items"], 1):
            the_artist = info["artists"]
            for uri in the_artist:
                artists_uri = uri["uri"]
                return artists_uri
    else:
        return False
    
@app.route("/sms", methods = ["GET", "POST"])
def list_of_songs():
    '''
    Prints a list of the top 10 songs from the artist given via text as well 
    as the track number and album it is in, if the artist can be found.
    
    '''
    client_credentials_manager = SpotifyClientCredentials(get_key('Client_ID'), get_key('Client_Secret'))
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    artist = request.form["Body"]
    artist_uri = get_artists_uri(artist,sp)
    
    response = MessagingResponse()
    
    if artist_uri:
        top_tracks = sp.artist_top_tracks(artist_id = artist_uri)
        
        message = "\n {}'s top 10 songs are: \n".format(artist)      
        for count, info in enumerate(top_tracks["tracks"], 1):
            if info["album"]["album_type"] == "single":
                message += "\n{} {}\n\t A single".format(count, info["name"])
            else:
                message += "\n {} {}\n\tTrack {} on {}".format(count, info['name'], info['track_number'], info['album']['name'])
    else:
        message = "\nThere is no artist by this name."
        
    response.message(message)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)