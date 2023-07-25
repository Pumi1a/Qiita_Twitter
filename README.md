[English README is here](https://github.com/Pumi1a/Qiita_Twitter/blob/main/README-en.md)

Qiita にも記事として投稿してあります。記事リンクは[こちら](https://qiita.com/Pumila/items/b09b1f8532e129e1b16d)から。

## はじめに
Qiita の記事の中からランダムで Twitter に投稿するシステムを構築しました。ランダムといっても完全ランダムではなく、音楽プレイヤーのシャッフルをリピートしている感じになります。同じ記事が連投されたり、偏ったりすることがありますからね。Qiita に投稿してある記事のリストを保持し、それをシャッフルして Twitter に投稿し、全ての記事が投稿されたら、最初に戻りまたシャッフルして Twitter に投稿することを繰り返す流れになります。

## 環境
* Raspberry Pi 4 Model B
    * CentOS Stream 8
        * Python 3.11.0
            * tweepy 4.14.0
            * requests 2.28.2

## 導入
ラズパイなどのサーバを持っていない方はホスティングサービスの利用を検討してみて下さい。無料で使えるホスティングサービスについては以下記事にまとめてあります。使い方については、以下記事の参考を参照して下さい。私は Railway にて稼働させています。

https://qiita.com/Pumila/items/f66053143c4255f1de18

https://qiita.com/Pumila/items/29f26fb349d5592046ae

### Qiita アクセストークンの取得
[Qiita](https://qiita.com) の右上の自分のアイコンから[設定]→[アプリケーション]→[[新しくトークンを発行する](https://qiita.com/settings/tokens/new)]（このリンクからも飛べます）
![1.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/9ed9854a-02e2-0afc-1b34-f39c9685a33d.png)
アクセストークンの発行ページに飛べたら、適当に名前をつけて、スコープとして最適なものを選択して下さい。Qiita Team とやらが何なのか私は知りませんが、使ってはいないので `read_qiita` だけ選択し発行します。
![2.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/5bdec186-9d3b-49a5-6567-d17ea74abbaf.png)
アクセストークンは 1 度しか表示されないのできちんとメモするのを忘れないようにして下さい（まあ、忘れても再発行すればいいんですが…）。これで、アクセストークンの取得は完了です。

### Twitter API の取得
続いて、Twitter API の取得に移っていきます。[Twitter Developer Portal](https://developer.twitter.com/en/portal/petition/essential/basic-info) にアクセスし、`Sign up for Free Account` を押下します（~~月額 100$ なんて払えるわけないだろ！ふざけてんのか？~~）。
![3.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/60f9d945-b480-b996-9744-08c1d0e9b3be.png)
以下のように Twitter API をどのように使うのか聞かれますので、適当に ChatGPT くんを用いて生成させましょう（250文字以上制限があります）。
私は以下のように記載しました（ほとんどこの内容は見てないのではなかろうか…）。ChatGPT くんは壮大な内容に膨らませてくれますね…まあいいでしょう。あとは全てチェックして、[Submit] を押下して下さい。
*I plan on leveraging the Twitter API to create an automated system that will tweet the articles I post on Qiita. The idea is to build a bridge between these two platforms, providing an efficient way to simultaneously share my knowledge with both my Twitter followers and Qiita readers. By doing so, I hope to expand the reach of my articles beyond just the Qiita community, making them accessible to a wider audience through Twitter. This not only enhances the visibility of my content, but also potentially fosters engaging discussions among users of both platforms. I believe that this integration could greatly streamline my sharing process and help cultivate a more interconnected community around the content I publish.*
![4.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/470a2123-30b9-9360-7fdc-6c602f9672d6.png)
すると、すぐにダッシュボードに移ると思います（本当に内容見てるのか？適当に書いても問題ないのでは…）。ダッシュボードから [+ Create Project] を選択します。
![5.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/6216c144-5ab4-b0fe-08b7-e12268996656.png)
適当に名前を入力して次へ、 使い方として、[Makeing a bot] を選択し次へ、プロジェクトの説明も適当に入力して次へを選択して下さい。アプリケーションの名前の入力を求められるのでここでも適当に入力して次へ進んで下さい。
`API Key` と `API Key Secret` が表示されるので、これをメモしておいて下さい。`Bearer Token` は特に使いません。メモしたら、[App Settings] を押下して下さい。
![7.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/7477cd7e-c9c2-f987-dddd-90beaa7bd11f.png)
以下のような画面に遷移するので、`User authentication settings` から [Set up] を選択して下さい。
![8.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/3a960c1d-8e54-cedc-946d-42390493f5f4.png)
アプリ権限としては、`Read and write` を選択して下さい。
![9.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/a21dd5de-f532-c3f2-72da-c44a440fe64f.png)
アプリの種類はどちらでもいいと思いますが、`Native App` を選択して下さい。
![10.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/90147137-670f-5625-1118-f23f4a9a4649.png)
最後にアプリ情報として、 `Callback URI / Redirect URL` と `Website URL` を設定して下さい。Qiita のホームページを登録しておけばいいと思います。
![11.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/9d78c7e3-d3c0-b911-ecf2-754bbfae7f10.png)
設定が完了すると `Client ID` と `Client Secret` が表示されますが、今回は使用しないので、特にメモする必要はありません（あくまで自己責任で）。
![12.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/bc08ab60-763c-d5b9-dd23-da89d5f3491b.png)
続いて、`Settings` の隣にある `Keys and tokens` を選択し、`Access Token and Secret` の [Generate] を押下して下さい。
![13.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/9d068550-1cec-8930-72c7-f03fafe34600.png)
すると、以下のように　`Access Token` と `Access Token Secret` が発行されるので、メモしておきましょう。
![14.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/bdcf7d8b-a241-e63c-168d-0b63b39951d1.png)
最後に確認として、`Access Token and Secret` の権限がきちんと `Created with Read and  Write permissions` となっていることを確認して下さい。この権限に <font color="Red">`Write`</font> が含まれていない場合は、`User authentication settings` の設定が間違えている可能性があります。再度設定を見直して、`Access Token and Secret` を再発行して下さい。
![16.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/0c1d1307-672e-bae2-d98e-85e51fd5c78d.png)
これで、Twitter API を利用するために必要な情報が揃いました。いよいよ実装に移っていきましょう。

### 実装
ソースコードの流れを簡単に説明していきます。`get_all_posts()` 関数では Qiita に投稿してある全ての記事を取得します。`post_tweet(message)` 関数では受け取った `message` を Twitter に投稿してくれます。最後に `main()` 関数では取得した全記事の中から、タイトルと URL 、タグを取得します。そして、`zip()` 関数を用いてリストをまとめてから、シャッフルします。その後ループの中で、`message` を作成し（なるべく Qiita のお作法に従いました。お好みで修正して下さい）、`post_tweet()` 関数を呼び出してツイートし 1 時間待機します。フリーアカウントだと月に 1,500 ツイートできるみたいなので、待機時間は最短で 28.8 分まで短縮することが可能です（こちらもお好みで修正して下さい）。
![17.PNG](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/1115291/8a87d3a4-e8bb-f855-4c4d-f5e006c8f593.png)
続いて各変数について説明していきます。
上 4 つは Twitter API に関するものです。最後の `BEARER` は Qiita のアクセストークンになります。
* `CONSUMER_KEY`：`API Key`
* `CONSUMER_SECRET`：`API Key Secret`
* `ACCESS_TOKEN`：`Access Token`
* `ACCESS_TOKEN_SECRET`：`Access Token Secret`
* `BEARER`：Qiita のアクセストークン

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

## 最後に
Qiita の記事の中からランダムで Twitter に投稿する機能を実装してみました。これで、定期的に Twitter に Qiita の記事が投稿されるので、少しでも皆様の目に届くことを期待しています。Github に Dokerfile ごとアップロードしているので、こちらからデプロイすることも可能です。良き Twitter ライフを。

https://github.com/Pumi1a/Qiita_Twitter

## 参考
[【TwitterAPI】note記事を自動投稿するPythonコードを作ってみた](https://note.com/bunsekiya_tech/n/n473884d9c843)



