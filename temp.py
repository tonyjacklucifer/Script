import requests
from instagrapi import Client
from pymongo import MongoClient
import os
import time

# MongoDB setup
mongo_client = MongoClient("mongodb+srv://tonyjacklucifer123:tonyjacklucifer@cluster.a3okr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster")
db = mongo_client['test']
collection = db['videos']

# Initialize the Instagram client
client = Client()
client.login('diiishaaa_07', 'Disha@007')

def upload_reel(reel):
    url = reel['videoUrl']
    caption = reel['caption']

    # Download the video
    response = requests.get(url)
    video_path = "video.mp4"  # Temporary local file name
    with open(video_path, 'wb') as file:
        file.write(response.content)

    # Upload the video as a reel
    client.video_upload(video_path, caption=caption)

    # Clean up
    os.remove(video_path)

    # Delete the document from the database
    collection.delete_one({'_id': reel['_id']})

def job_930am():
    # Fetch the first reel
    reel = collection.find_one()  # Modify this query as needed
    if reel:
        upload_reel(reel)

def job_830pm():
    # Fetch the second reel
    reel = collection.find_one()  # Modify this query as needed
    if reel:
        upload_reel(reel)

# Directly call job_830pm
job_830pm()

# If you want to keep the script running for future calls, you can add a sleep or similar logic
# For example:
while True:
    time.sleep(60)  # Keep the script running; adjust as needed
