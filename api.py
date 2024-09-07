# fetching songs data from spotify api

import spotipy as sp
from spotipy.oauth2 import SpotifyOAuth
import numpy as np


negativeset = [2, 5, 14, 16, 20, 23, 25, 28, 31, 36]
class API:
    def __init__(self, client_ID, client_secret, scope, timerange, tracks, tracklimit):
        self.client_ID = client_ID
        self.client_secret = client_secret
        self.scope = scope
        self.access_token = self.get_access_token()
        self.sp = self.authenticate(self.scope)
        self.limit = tracks.limit
        self.timerange = timerange
        self.tracklimit = tracklimit

    

    def delete_comma(self, list):
        list = list[:-2]
        return list

    
    def authenticate(self, scope):
        spotifyoauth = SpotifyOAuth(client_id = self.client_ID, client_secret = self.client_secret, scope = scope, redirect_uri = 'http://localhost:8888/callback')
        one = sp.Spotify(auth_manager=spotifyoauth)
        return one

    def get_access_token(self):
        one = sp.oauth2.SpotifyClientCredentials(client_id=self.client_ID, client_secret=self.client_secret)
        access_token = one.get_access_token(as_dict=False)
        return access_token
    
    def fetch_audio_features(self, ids):
        attributes = ["danceability", "energy", "loudness", "acousticness", "valence", "tempo"]
        # this returns a list of audio features
        featurelist = self.sp.audio_features(ids)
        tracknumber = len(featurelist)
        # for every song
        vectors = []
        for i in range(tracknumber):
            vector = []
            for attribute in attributes:
                if featurelist[i] is not None:
                    number = featurelist[i][attribute]
                    vector.append(number)
            vector = np.array(vector)
            vectors.append(vector)
        return vectors
    
    # good
    def fetch_track_features(self, ids):
        length = len(ids)
        features = []
        # limit is 100, if there are more than 100 tracks, need to do it seperately
        while length > 98:
            limitids = ids[0:98]
            # this should be 99
            ids = ids[98:]
            length = len(ids)
            feature = list(self.fetch_audio_features(limitids))
            features.extend(feature)
        if length <= 98:
            feature = list(self.fetch_audio_features(ids))
            features.extend(feature)
            
        return features
        

    def get_top_tracks_rawdata(self):
        result = self.sp.current_user_top_tracks(limit = self.limit, time_range = self.timerange)
        return result
    

    def spotipy_tracks(self, ids):
        result  = self.sp.audio_features(ids)
        return result

    
    def get_top_tracks_names(self):
    # upper limit 50
        songs = []
        # initialize spotifyoauth to prepare for authentication, get teh acess token as well
        track = self.get_top_tracks_rawdata(self.timerange)['items']
        for index, item in enumerate(track):
            songs.append(f"{item['name']}--{index + 1} by ")
            for i in range(len(item['artists'])):
                if item['artists'][i] is not None:
                    songs[-1] += f"{item['artists'][i]['name']}, "
            if songs[-1][-2] == ',':
                songs[-1] = self.delete_comma(songs[-1])
        return songs

    # getting teh top tracks id as a list
    def get_top_ids(self):
        id = []
        result = self.get_top_tracks_rawdata()
        for i in range(self.limit):
            id.append(result['items'][i]['id'])
        return id
    

    def get_categories(self):
        # maybe change limit later, but this limit is different from the rest
        try:
            categories = self.sp.categories(limit=self.tracklimit)
            ids = []
            # i here can be changed to get different categories's ids
            for i in range(self.tracklimit):
                ids.append(categories['categories']['items'][i]['id'])
            # return a list of category ids
            return ids
        except sp.exceptions.SpotifyException as e:
            if e.http_status == 400:
                print(f"error: {e}")
    

    # get the playlist ids for the negative set
    def get_negative_category(self):

        categories = []
        # get all teh categories for the negative set
        for item in negativeset:
            categories.append(self.get_categories()[item])
        return categories

    # instead of taking the category id, call the get categories function and get the id directly 
    def get_playlist_id(self, categories):
        # this returns a list of
        ids = []
        for category in categories:
            # playlist id of each category
            playlist = self.sp.category_playlists(category)
            id = playlist['playlists']['items'][0]['id']
            ids.append(id)
        # return a list of playlist ids
        return ids


    # recommended ids
    def get_tracks_id(self, categories) :
        playlists = {}
        # a list of ids
        ids = self.get_playlist_id(categories)
        for id in ids:
            playlist = self.sp.playlist(id)
            names = playlist['tracks']['items']
            for i in range(len(names)):
                playlists[names[i]['track']['id']] = names[i]['track']['name']
        # return a dict with playlists
        return playlists
    
    def get_liked_songs(self, scope):
        one = self.authenticate(scope)
        count = 0
        songs = []
        if count < 731:
            limit = 50
        else:
            limit = 791 - count
        while count < 791:
            playlists = one.current_user_saved_tracks(limit=limit, offset=count)
            count = count + limit
            names =  playlists['items']
            for i in range(len(names)):
                songs.append(names[i]['track']['id'])
        return songs
        
    def get_liked_vectors(self):
        # returns a list of ids
        ids = self.get_liked_songs(scope='user-library-read')
        vectors = self.fetch_track_features(ids)
        return vectors


    # new ones everyday
    def create_playlist(self, trackids, new_scope = 'playlist-modify-private'):
        one = self.authenticate(new_scope)
        user = one.current_user()
        userid = user['id']
        list = one.user_playlist_create(userid, "neural test 1", public=False, collaborative=False)
        listid = list['id']
        # change this for neural 
    
        one.user_playlist_add_tracks(userid, listid, trackids)

    def negativeset(self):
        categories = self.get_negative_category()
        playlistdict = self.get_tracks_id(categories)
        ids = []
        for item in playlistdict:
            ids.append(item)
        vectors = self.fetch_track_features(ids)
        return vectors
    
