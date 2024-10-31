import requests
from instagrapi import Client
from pymongo import MongoClient
import os
import schedule
import time

# MongoDB setup
mongo_client = MongoClient("mongodb+srv://tonyjacklucifer123:tonyjacklucifer@cluster.a3okr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster")
db = mongo_client['test']
collection = db['videos']

# Initialize the Instagram client
client = Client()
client.login('rooohaaan_07', 'Disha@007')

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

# Schedule the jobs
schedule.every().day.at("09:30").do(job_930am)
schedule.every().day.at("20:30").do(job_830pm)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(60)  # Wait a minute before checking again