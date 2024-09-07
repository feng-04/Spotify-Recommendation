import numpy as np
import base64
from api import API
from tracks import Tracks
from datas import datas
import tensorflow as tf
import sys

# keys
client_ID = 'ClientID Here'
client_secret =  'ClientSecret Here'
credential = f"{client_ID}:{client_secret}"
bytes = credential.encode('ascii')
encoded = base64.b64encode(bytes).decode('ascii')



attributes = ["danceability", "energy", "loudness", "acousticness", "valence", "tempo"]



def main():
    scope = 'user-top-read'
    timerange = "long_term"
    tracks = Tracks(50)
    spotifyapi = API(client_ID=client_ID, client_secret=client_secret, scope=scope, timerange=timerange, tracks=tracks, tracklimit=10)
    data = datas()
    # convert it into a 2d array
    recommendedvectors = np.array(tracks.recommended_vectors(spotifyapi))

    if len(sys.argv) != 2:
        print("Error, please enter the model name")
        return
    
    predict_indices = []
    model = tf.keras.models.load_model(sys.argv[1])
    probabilities = model.predict(recommendedvectors)
    for i in range(len(probabilities)):
        if probabilities[i] > 0.56:
            predict_indices.append(i)
    
    categories = spotifyapi.get_categories()
    playlist = spotifyapi.get_tracks_id(categories)
    tracksid = list(playlist.keys())
    goodids = []

    for index in predict_indices:
        goodids.append(tracksid[index])
    
    spotifyapi.create_playlist(goodids)

    

   
main()


