# TwitterAPIv2-Webhooks-Discord-BOT
Twitter API v2を使用し特定のハッシュタグやユーザーのツイートをStream APIを使いリアルタイムに取得する。<br>
その後TweetLinkに変換し、WebhooksでDiscordの指定チャンネルに送信<br>

## TweetLinkの構造 <br>
```https://twitter.com/<tweet_username>/status/<tweet_id>```
## Discord Webhooks 指定項目 <br>
```python
{
  "username": "<tweet_username>",
  "avatar_url": "<profile_image_url>",
  "content": "https://twitter.com/<tweet_username>/status/<tweet_id>"
}
```