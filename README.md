# Spotify-Recommendation
This project leverages Spotify’s Web API to deliver personalized music recommendations.

While it’s possible to implement a centralized authentication system for seamless access, users currently need to obtain their own API credentials (Client ID and Secret) to use the application.

Setup Instructions:
Go to the Spotify Developer Dashboard, https://developer.spotify.com/, and log in.
Create a new app, with an application name and desciption. For Redirect url, simply enter http://localhost:8888/callback
Obtain your Client ID and Client Secret.
Input these credentials into the respective variable names main.py

Note:
This approach prioritizes user privacy and complies with Spotify’s API policies. While a more integrated authentication system could enhance user experience, I chose this method to maintain simplicity and focus on the core functionalities of the application, namely the data manipulation and the machine learning functionalities.

The get_dot function in tracks.py is from an earlier build of the project, which represents each song as vector in R6 and seeks to find similar music by computing the dot products between two songs. The function is left in the code as it allows the user to create two different playlists from two different methods, in order to better understand the advantages and disadvantages of each method

