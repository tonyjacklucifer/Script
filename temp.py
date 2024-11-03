import requests
from instagrapi import Client
from pymongo import MongoClient
import os
import time
import imaplib
import email
import re

# MongoDB setup
mongo_client = MongoClient("mongodb+srv://tonyjacklucifer123:tonyjacklucifer@cluster.a3okr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster")
db = mongo_client['test']
collection = db['videos']

# Initialize the Instagram client
client = Client()

def get_otp(email_user, email_pass):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(email_user, email_pass)
    mail.select('inbox')

    # Search for the latest OTP email
    result, data = mail.search(None, 'ALL')  # Adjust search criteria as needed
    email_ids = data[0].split()
    latest_email_id = email_ids[-1]  # Get the latest email
    result, data = mail.fetch(latest_email_id, '(RFC822)')
    
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Extract the OTP from the email body
    body = msg.get_payload(decode=True).decode()
    otp = extract_otp_from_body(body)

    mail.logout()
    return otp

def extract_otp_from_body(body):
    match = re.search(r'\b\d{6}\b', body)  # Adjust this regex to find the OTP
    return match.group(0) if match else None

def login_with_otp(username, password, email_user, email_pass):
    try:
        client.login(username, password)
    except Exception as e:
        if 'ChallengeRequired' in str(e):
            print("Challenge required. Fetching OTP...")
            otp = get_otp(email_user, email_pass)
            if otp:
                print(f"Using OTP: {otp}")
                client.challenge_resolve(otp)
            else:
                print("OTP not found!")
                return False
    return True

# Update with your email credentials
email_user = os.getenv('EMAIL')  # Your email
email_pass = os.getenv('EMAIL_PASSWORD')  # Your email password

# Log in
if login_with_otp('diiishaaa_07', 'Disha@007', email_user, email_pass):
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


    def job_830pm():
        reel = collection.find_one()  # Modify this query as needed
        if reel:
            upload_reel(reel)

    # Directly call job_830pm
    job_830pm()

    # Keep the script running for future calls
    while True:
        time.sleep(60)  # Keep the script running; adjust as needed
else:
    print("Login failed.")
