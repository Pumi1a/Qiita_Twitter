#!/usr/bin/env python3
import os
import random
import time
import requests
import tweepy

def get_all_posts():
    page = 1
    per_page = 100
    all_posts = []
    
    while True:
        response = requests.get(f'https://qiita.com/api/v2/authenticated_user/items?page={page}&per_page={per_page}', headers=headers)
        posts = response.json()
        if posts:
            all_posts.extend(posts)
            page += 1
        else:
            break

    return all_posts

def post_tweet(message):
    client = tweepy.Client(consumer_key=CONSUMER_KEY, 
    consumer_secret=CONSUMER_SECRET, access_token=ACCESS_TOKEN, 
    access_token_secret=ACCESS_TOKEN_SECRET)
    
    client.create_tweet(text = message)

def main():
    titles = []
    urls = []
    tags = []
    while True:
        try:
            posts = get_all_posts() 
            for item in posts:
                titles.append(item['title'])
                urls.append(item['url'])
                tags.append(item['tags'])
            combined_lists = list(zip(titles,urls,tags))
            random.shuffle(combined_lists)
            for item in combined_lists:
                tag_message = ""
                for tag in item[2]:
                    tag_message += f"#{tag['name']} "
                message = f"{item[0]}\n{item[1]} #Qiita {tag_message} @Pumi1aより"
                post_tweet(message)
                time.sleep(3600)  # Wait for 1 hour

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(60)  # Wait for 1 minute before trying again

if __name__ == "__main__":
    # Twitter API credentials
    CONSUMER_KEY = os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

    BEARER = os .getenv("BEARER")
    headers = {
        'Authorization': f'Bearer {BEARER}'
    }
    main()
