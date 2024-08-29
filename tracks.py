import numpy as np


class Tracks:
    def __init__(self, limit):
        self.limit = limit

    # getting the top tracks id 
    def get_vectors(self, spotifyapi, ids):
        attributes = ["danceability", "energy", "loudness", "acousticness", "valence", "tempo"]
        # use the feature list to get teh ids, for either top or recommended, depending on the ids putitng into it
        # ideas: motify it so that the get_ids functions can handle both tip and recommended-----problem: one is playlist, one is not, so need two
        featurelist = spotifyapi.fetch_track_features(ids)
        features = []
        length = len(featurelist)
        # for every song
        for i in range(length):
            vector = []
            for attribute in attributes:
                number = featurelist[i][attribute]
                vector.append(number)

            vector = np.array(vector)
            features.append(vector)
        features = np.array(features)
        for i in range(len(features)):
            features[i] = self.normalize(features[i])
        return features
    
    def recommended_vectors(self, spotifyapi):
        categories = spotifyapi.get_categories()
        recommended = spotifyapi.get_tracks_id(categories)
        recommendedids = list(recommended.keys())
        recommendedvectors = spotifyapi.fetch_track_features(recommendedids)
        return recommendedvectors

    # topvectors would be one object under class, and recommended vectors would be anotherone
    def get_dots(self, spotifyapi):

        topids = spotifyapi.get_top_ids()
        topvector = spotifyapi.fetch_track_features(topids)
        topvectors = list(topvector)
        # now returns
        # get the recommended categories
        categories = spotifyapi.get_categories()
        recommended = spotifyapi.get_tracks_id(categories)
        recommendedids = list(recommended.keys())
        recommendedvectors = spotifyapi.fetch_track_features(recommendedids)
        dots = {}
        lenstop  = len(topvectors)
        lensre = len(recommendedvectors)
        for i in range(lenstop):
            for j in range(lensre):
                angle = self.get_angle(topvectors[i], recommendedvectors[j])
                dots[f"{i}/{j}"] = angle
        return dots
    

    def normalize(self, v1):
        n1 = np.linalg.norm(v1)
        v1 = v1 / n1
        return v1

    def get_angle(self, v1, v2):
        dotproduct = np.dot(v1, v2)
        n1 = np.linalg.norm(v1)
        n2 = np.linalg.norm(v2)
        cos = dotproduct / (n1 * n2)
        angle = np.arccos(np.clip(cos, -1.0, 1.0) )
        return np.degrees(angle)
    
    # pass in spotifyapi, top vectors and recommended vectors which are objects of tehsame class
    # needs dots, the dot product between top and recommened, also need playlist 
    def get_goodid_dots(self, spotifyapi):
        hopefullygood = []
        dots = self.get_dots(spotifyapi=spotifyapi)
        # returns a dict
        categories = spotifyapi.get_categories()
        playlist = spotifyapi.get_tracks_id(categories)
        for pairs, angle in dots.items():
            if angle < 0.2000:
                # bad when limit goes beyond 10, since this one only takes away the first 2 characters, for 0-9, it's 1 number and /, so doesnt work when 10/, cant int
                # iterating through each key, to isolate recommended
                ind = pairs.split('/')[1]
                index = int(ind)
                hopefullygood.append(index)
        final = list(set(hopefullygood))
        # all the songs that supposely are close to any of my top 10 tracks
        final.sort()
        trackids = []
        for key in playlist.keys():
            trackids.append(key)
        finalids = []
        for index in final:
            finalids.append(trackids[index])
        return finalids
    
    