#!/usr/bin/env python3

"""
Chirp - Automated Twitter Photo Bot

Copyright (c) 2025 Alessandro Chitarrini

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import tweepy
from dotenv import load_dotenv
from datetime import datetime
import shutil

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

def get_twitter_api():
    """Authenticate and return a tweepy API object."""
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)

def log_post_action(photo_filename, status):
    """Log the action of posting a photo to a log file."""
    with open("post_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: {status} photo '{photo_filename}'\n")

def move_photo(photo_filename, target_dir):
    """Move the photo to the specified target directory."""
    os.makedirs(target_dir, exist_ok=True)  
    photo_path = os.path.join("photos", photo_filename)
    new_photo_path = os.path.join(target_dir, photo_filename)
    try:
        shutil.move(photo_path, new_photo_path)
        print(f"Moved photo to {target_dir} directory: {new_photo_path}")
    except Exception as e:
        print(f"Failed to move photo: {e}")

def post_photo(photo_filename):
    """Post a specific photo from the photos directory."""
    media_path = os.path.join("photos", photo_filename)
    
    api = get_twitter_api()
    
    try:
        media = api.media_upload(filename=media_path)
        media_id = media.media_id_string
        
        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
        
        response = client.create_tweet(text="", media_ids=[media_id])
        print(f"Successfully posted tweet with media ID: {media_id}")
        
        log_post_action(photo_filename, "Posted")
        
        move_photo(photo_filename, "posted_photos")
        
        return True 
        
    except Exception as e:
        print(f"Failed to post photo: {e}")
        return False  

def post_random_photo(max_attempts=3):
    """Attempt to post a photo from the photos directory."""
    attempts = 0
    
    while attempts < max_attempts:
        photos = os.listdir("photos")
        
        if not photos:
            print("No photos found in the directory. Waiting for new photos...")
            break  
        
        photo_to_post = photos[0]
        
        if post_photo(photo_to_post):
            break
        else:
            move_photo(photo_to_post, "photos_rejected")
            log_post_action(photo_to_post, "Rejected")
            attempts += 1
            print(f"Retrying with the next photo... Attempt {attempts}/{max_attempts}")

def main():
    post_random_photo()

if __name__ == '__main__':
    main()