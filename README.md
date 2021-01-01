# TwitterAPIv2-Webhooks-Discord-BOT
Twitter API v2を使用し特定のハッシュタグやユーザーのツイートをStream APIを使いリアルタイムに取得する。<br>
その後TweetLinkに変換し、WebhooksでDiscordの指定チャンネルに送信<br>

## Twitter Steram API v2 取得データ構造
```json
{
    "data": {
        "author_id": "<tweet_user_id>",
        "created_at": "<post_date>",
        "id": "<tweet_id>",
        "text": "<tweet_content>"
    },
    "includes": {
        "users": [
            {
                "id": "<tweet_user_id>",
                "name": "<tweet_user_screen_name>",
                "profile_image_url": "<profile_image_url>",
                "username": "<tweet_user_name>"
            }
        ]
    },
    "matching_rules": [
        {
            "id": "<rules_id1>",
            "tag": "<tag_name_1>"
        },
        {
            "id": "<rules_id2>",
            "tag": "<tag_name_2>"
        }
    ]
}
```
## TweetLinkの構造 <br>
```https://twitter.com/<tweet_username>/status/<tweet_id>```
## Discord Webhooks 指定項目 <br>
```python
{
  "username": "<tweet_user_name>",
  "avatar_url": "<profile_image_url>",
  "content": "https://twitter.com/<tweet_user_name>/status/<tweet_id>"
}
```
## test