import requests
import json
import time

import config

wh1 = config.wh1
wh2 = config.wh2
wh3 = config.wh3
wh4 = config.wh4
wh5 = config.wh5
#webhook_url_35P_Art = os.getenv("35P_Art")
#webhook_url_Admin_twitter = os.getenv("Admin_twitter")

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token):
    # You can adjust the rules if needed
    #ツイート取得条件設定
    #以下の設定はその一例です
    #設定方法はTwitterAPIv2のリファレンスに詳しく記載されています
    #簡単な説明
    #{"value": "(検索ワード) (検索条件)", "tag": "タグの名前"},でセットです
    #(検索ワード)のところには取得したいツイートに含まれるワードを指定できます 例:"(さくらみこ)", "(#さくらみこ)", "(さくらみこ OR みこなま)", "(さくらみこ AND みこなま)"
    #(検索条件)にはリツイートを取得しない、引用リツイートを取得しない、画像や動画などのメディアなどを含む物だけ取得…などなど細かく設定することが可能です。
    #例:(-is:retweet)←リツイートを取得しない設定　"-is:…"の"-"は動作を反転させるつまり(is:retweet)とするとリツイートのみを取得するようになる
    #同様に引用リツイートを取得しない(-is:quote)や画像や動画のみを取得したい場合に使うhas:media)なども設定できる
    sample_rules = [
        {"value": "(さくらみこ OR #みこなま OR みこらじお OR みこクラ OR  #みこきいたぞ OR #さくらみこ新3Dお披露目 OR #さくら色Dreamer) (-is:retweet)", "tag": "mikoti-Tweet"},
        {"value": "(#miko_Art OR #ミコミコ動画 OR #さくらみこMMD) (has:media -is:retweet -is:quote)", "tag": "35P-Art"},
        {"value": "(みこち OR みこち撮ったにぇ OR 35P鯖 OR さくら組料理部 OR #35P OR みこぴー OR mこち OR 35PProject OR 35PLAT OR みこቻ) (-is:retweet)", "tag": "35P-Tweet"},
        {"value": "(みっころね OR ぺこみこ OR わたみこ OR みこフレ OR miComet OR バブライブ OR みこマリ OR そらみこ OR #mikofla OR #ホロライブGTA OR #ホロAmongUs) (-is:retweet)", "tag": "collaboration"},
        #{"value": "(#ホロお正月CUP OR #ゆくホロくるホロ2020 OR #ホロライブ正月衣装) (-is:retweet)", "tag": "holo-2021"},
        #{"value": "(#ホロお正月CUP) (-is:retweet)", "tag": "holo-2021"},
        {"value": "from:sakuramiko35", "tag": "Miko"},
        #{"value": "from:ipms_IA -is:retweet", "tag": "test"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(headers, set, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?tweet.fields=created_at&expansions=author_id&user.fields=username,name,profile_image_url", headers=headers, stream=True,
    )
    print(response.status_code)
    if response.status_code==429:
        print("ストリームを開始出来ませんでした。")
        return
        
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
        
    for response_line in response.iter_lines():
        if response_line:

            json_response = json.loads(response_line)
            
            # 辞書データから所望の値を取り出す
            tweet_id = json_response["data"]["id"]
            users_name = json_response["includes"]["users"][0]["name"]
            profile_image_url = json_response["includes"]["users"][0]["profile_image_url"].replace("_normal", "")
            tweet_user_id = json_response["includes"]["users"][0]["username"]
            matching_rules = json_response.get("matching_rules")
            matching_rules_tag = [d.get('tag') for d in matching_rules]
            
            print(matching_rules_tag)
            print(users_name)
            #print(profile_image_url)
            #print(tweet_user_id)
            #print(tweet_id)

            tweetlink = "https://twitter.com/{}/status/{}"
            tweetlink_content = tweetlink.format(tweet_user_id, tweet_id)
            print(tweetlink_content)

            post_content = {
                  "username": users_name,
                   "avatar_url": profile_image_url,
                  "content": tweetlink_content
            }
            
            #if "mikoti-Tweet" in matching_rules_tag:
            #    print("post 配信感想")
            #    requests.post(wh1, post_content)
            if "35P-Art" in matching_rules_tag:
                print("post miko_Art")
                requests.post(wh2, post_content)
            if "35P-Tweet" in matching_rules_tag or "mikoti-Tweet" in matching_rules_tag:
                print("post 35Pツイート")
                requests.post(wh3, post_content)
            if "collaboration" in matching_rules_tag:
                print("post コラボツイート")
                requests.post(wh4, post_content)
            if "Miko" in matching_rules_tag:
                print("post みこちった〜")
                requests.post(wh5, post_content)
                

def main():
    try:
        bearer_token = config.token
        headers = create_headers(bearer_token)
        rules = get_rules(headers, bearer_token)
        delete = delete_all_rules(headers, bearer_token, rules)
        set = set_rules(headers, delete, bearer_token)
        get_stream(headers, set, bearer_token)
    except:
        return

if __name__ == "__main__":
    while True:
        main()
        print("Twitterサーバーとの接続が切断されたため、2分後に再接続します。")
        time.sleep(120)
