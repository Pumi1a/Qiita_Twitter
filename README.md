[日本語版 README はこちら](https://github.com/Pumi1a/Qiita_Twitter/blob/main/README-ja.md)

## Introduction
I have built a system that posts articles from Qiita to Twitter in a random manner. However, it's not entirely random, it's more like repeating the shuffle feature on a music player. This is because the same articles might be posted repeatedly or there might be a bias. The system holds a list of articles posted on Qiita, shuffles them, and posts them to Twitter. When all articles have been posted, it returns to the beginning, reshuffles, and continues to post.

Qiita is a Japanese information sharing site. Therefore, it might be a good idea to automatically post about personal blogs on Twitter or post articles from Stack Overflow.

## Environment
* Raspberry Pi 4 Model B
  * CentOS Stream 8
    * Python 3.11.0
      * tweepy 4.14.0
      * requests 2.28.2

## Implementation
If you don't have a server like Raspberry Pi, you might want to consider using a hosting service. Information about free hosting services can be found in the following article. Please refer to the following article for how to use them. I am running it on Railway.

https://qiita.com/Pumila/items/f66053143c4255f1de18

https://qiita.com/Pumila/items/29f26fb349d5592046ae

### Obtaining a Qiita Access Token
From your icon in the upper right corner of [Qiita](https://qiita.com), go to [Settings] → [Applications] → [[Generate new token](https://qiita.com/settings/tokens/new)] (You can also jump from this link)

![1.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/9ed9854a-02e2-0afc-1b34-f39c9685a33d.png)

Once you get to the access token issuance page, please give it a suitable name and select the appropriate scope. I'm not sure what Qiita Team is, but since I'm not using it, I'll select `read_qiita` and issue it.

![2.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/5bdec186-9d3b-49a5-6567-d17ea74abbaf.png)

Please make sure to take a note of the access token as it is displayed only once (well, you can reissue it if you forget it...). With this, the acquisition of the access token is complete.

### Obtaining the Twitter API
Next, let's move on to obtaining the Twitter API. Access the [Twitter Developer Portal](https://developer.twitter.com/en/portal/petition/essential/basic-info) and click on Sign up for Free Account (~~there's no way I can afford to pay $100 a month! Are you kidding me?~~).

![3.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/60f9d945-b480-b996-9744-08c1d0e9b3be.png)

You will be asked how you plan to use the Twitter API, so let's generate an appropriate response using ChatGPT (there is a minimum character limit of 250). I wrote as follows (I doubt they read much of this content...). ChatGPT will help you come up with some grandiose details... well, that's okay. Then, check all the boxes and click [Submit].
*I plan on leveraging the Twitter API to create an automated system that will tweet the articles I post on Qiita. The idea is to build a bridge between these two platforms, providing an efficient way to simultaneously share my knowledge with both my Twitter followers and Qiita readers. By doing so, I hope to expand the reach of my articles beyond just the Qiita community, making them accessible to a wider audience through Twitter. This not only enhances the visibility of my content, but also potentially fosters engaging discussions among users of both platforms. I believe that this integration could greatly streamline my sharing process and help cultivate a more interconnected community around the content I publish.*

![4.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/470a2123-30b9-9360-7fdc-6c602f9672d6.png)

I suppose you'll be immediately redirected to the dashboard (Are you really looking at the content? Isn't it okay to just write anything...?). Select [+ Create Project] from the dashboard.

![5.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/6216c144-5ab4-b0fe-08b7-e12268996656.png)

Enter a random name and click next. For usage, select [Making a bot] and click next. Enter a random project description and click next. You will be asked to enter the name of your application, so enter anything here as well and proceed to the next step. The `API Key` and `API Key Secret` will be displayed, so please note them down. You will not particularly use the `Bearer Token`. After you have taken notes, please press [App Settings].

![7.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/7477cd7e-c9c2-f987-dddd-90beaa7bd11f.png)

You will be directed to a screen like the one below, so please select [Set up] from `User authentication settings`.

![8.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/3a960c1d-8e54-cedc-946d-42390493f5f4.png)

For application permissions, please select `Read and write`.

![9.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/a21dd5de-f532-c3f2-72da-c44a440fe64f.png)

As for the type of app, either will be fine, but please choose `Native App`.

![10.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/90147137-670f-5625-1118-f23f4a9a4649.png)

Finally, as application information, please set `Callback URI` / `Redirect URL and Website URL`. You can register the homepage of Qiita.

![11.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/9d78c7e3-d3c0-b911-ecf2-754bbfae7f10.png)

When the setup is complete, the `Client ID` and `Client Secret` will be displayed, but there is no need to take notes on this for this time (at your own risk).

![12.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/bc08ab60-763c-d5b9-dd23-da89d5f3491b.png)

Next, select `Keys and tokens` next to `Settings`, and press [Generate] under `Access Token and Secret`.

![13.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/9d068550-1cec-8930-72c7-f03fafe34600.png)

Then, `Access Token` and `Access Token Secret` will be issued like below, so let's take note of them.

![14.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/bdcf7d8b-a241-e63c-168d-0b63b39951d1.png)

Lastly, for confirmation, please ensure that the permissions of `Access Token and Secret` are correctly set to `Created with Read and Write permissions`. If the permission does not include <font color="Red">`Write`</font>, it is possible that the `User authentication settings` are incorrect. Please review your settings again and reissue your `Access Token and Secret`.

![16.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/0c1d1307-672e-bae2-d98e-85e51fd5c78d.png)

Now you have all the information necessary to use the Twitter API. Let's move on to the implementation.

### Implementation
I'll briefly explain the flow of the source code. The `get_all_posts()` function fetches all the articles posted on Qiita. The `post_tweet(message)` function posts the received `message` to Twitter. Finally, in the `main()` function, the title, URL, and tags are fetched from all the retrieved articles. Then, the lists are consolidated using the `zip()` function and shuffled. Afterwards, in the loop, a `message` is created (as much as possible, I adhered to Qiita's conventions. Please modify as you like), and the `post_tweet()` function is called to tweet and wait for 1 hour. Since a free account allows you to tweet up to 1,500 times a month, it's possible to shorten the wait time to a minimum of 28.8 minutes (please adjust as you like).

![17.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/8a87d3a4-e8bb-f855-4c4d-f5e006c8f593.png)

Next, let's explain about each variable. The top four are related to the Twitter API. The last one, `BEARER`, is the access token for Qiita.

* `CONSUMER_KEY`: `API Key`
* `CONSUMER_SECRET`: `API Key Secret`
* `ACCESS_TOKEN`: `Access Token`
* `ACCESS_TOKEN_SECRET`: `Access Token Secret`
* `BEARER`: `Qiita access token`

```python:main.py
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
                message = f"{item[0]}\n{item[1]} #Qiita {tag_message} @Pumi1aより" # 適宜変更して下さい。
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
```

## Finally
I have implemented a feature to post randomly from Qiita articles to Twitter. With this, Qiita articles will be regularly posted on Twitter, and I hope that they reach as many people as possible. I have uploaded everything including the Dockerfile to Github, so you can deploy from there. Wishing you a great Twitter life.

## References
[Tried creating a Python code to automatically post note articles using the TwitterAPI](https://note.com/bunsekiya_tech/n/n473884d9c843)





