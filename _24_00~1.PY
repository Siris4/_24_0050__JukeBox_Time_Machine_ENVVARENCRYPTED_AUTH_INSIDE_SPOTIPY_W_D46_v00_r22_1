
import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Setting up environment variables:
CLIENT_ID = os.environ.get('CLIENT_ID', 'Custom Message / Key does not exist')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', 'Custom Message / Key does not exist')
REDIRECT_URI = os.environ.get('REDIRECT_URI', 'Custom Message / Key does not exist')
SCOPE = os.environ.get('SCOPE', 'Custom Message / Key does not exist')

# Displaying environment variables for verification (optional):
print(f"The CLIENT_ID is: {CLIENT_ID}")
print(f"The CLIENT_SECRET is: {CLIENT_SECRET}")
print(f"The REDIRECT_URI is: {REDIRECT_URI}")
print(f"The SCOPE is: {SCOPE}")

# --------------------------------------- The HOT 100 Song List for the Date Specified ------------------------------- #

# Constants:
LIMIT_OF_MAXIMUM_SONGS_TO_DATA_SCRAPE = 5  # Set to a high number to fetch all songs
counter = 1

def is_valid_title(title):
    """Checks if the title text is valid."""
    unwanted_keywords = ['Songwriter', 'Producer']  # Add any more keywords as needed
    return not any(keyword in title for keyword in unwanted_keywords) and len(title) <= 50

user_date_input = input("Which year do you want to Time Travel to? Please type the date in this format: YYYY-MM-DD: ")
print(user_date_input)

response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_date_input}/")
if response.status_code != 200:
    print("Failed to retrieve data")
    exit()

html_doc = response.text
soup = BeautifulSoup(html_doc, 'html.parser')

# Initialize lists to hold song titles and artist names:
songs_and_artists = []

# Fetching all elements that could potentially contain song titles or artist names:
song_elements = soup.find_all(["h3", "span"], class_=["c-title", "c-label"])

# Initialize placeholders:
current_title = None

for element in song_elements:
    if 'c-title' in element['class']:
        title_text = element.get_text(strip=True)
        if is_valid_title(title_text):
            current_title = title_text  # Valid title found, proceed to find the corresponding artist:
    elif 'c-label' in element['class'] and current_title:
        artist_name_text = element.get_text(strip=True)
        if not any(char.isdigit() for char in artist_name_text):
            songs_and_artists.append((current_title, artist_name_text))
            current_title = None  # Reset current_title after pairing:

# Print the list of songs and artists:
print(f"\nSongs and Artists from {user_date_input}:")
for song, artist in songs_and_artists:
    print(f"Song {counter}: {song}, Artist {counter}: {artist}")
    counter += 1

# ----------------------------------- Spotify URL Generating Link for each song chosen ------------------------------- #

# User chooses track and artist:
track_name_chosen_by_user = "imagination"
artist_name_by_user = "gene wilder"

# Initializes Spotipy with user credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# Searches for the track
track_name = track_name_chosen_by_user
artist_name = artist_name_by_user
query = f"track:{track_name} artist:{artist_name}"
result = sp.search(q=query, type="track")

# Extracts the track URL
if result['tracks']['items']:
    track_url = result['tracks']['items'][0]['external_urls']['spotify']
    print(track_url)
else:
    print("Song not found.")
