import requests
import datetime
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='AAAAAAAAAAAAAAAAAAAAAJFEKgEAAAAAUmp%2F8yloASSlyjrrRbV%2BYu3MBE0%3DvHDl6YnmRYk7tx6LIjDjBknIDzUtB48lafGXGwku12qdTvbspH'
webhook_url_35P_tweet = 'https://discord.com/api/webhooks/794004355598385213/IJi3LhpDm5Z7M8pHuu1N13sAS_Tck6HOeKhyjUkmCLTDfsX8xQjt21q-I9nbTkcZeRCM'
webhook_url_35P_Art = 'https://discord.com/api/webhooks/794011767999168522/enQP6wjcO0YwQe948mSPNMV7QCbJA5mhwOvVBKKEKcmZsR7-AMcI87BTQVRBEmMMnFUy'
webhook_url_Admin_twitter = 'https://discord.com/api/webhooks/794011967462834196/1gBCG4prIJ4sdIDqJjmREt2FN75GzXNij_OfNfW7_b8yURdh5WUcXQiRNojP-4BqgaXy'


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
    sample_rules = [
        {"value": "(#さくらみこ OR #miko_Art OR #みこなま OR #ミコミコ動画 OR #みこらじお OR #さくら組料理部 OR #みこきいたぞ OR #バブライブ OR #さくらみこ新3Dお披露目 OR #さくらみこMMD) (-is:retweet -is:quote)", "tag": "35P-Tweet"},
        #{"value": "(#miko_Art OR #ミコミコ動画 OR #さくらみこMMD) (has:media -is:retweet -is:quote)", "tag": "35P-Art"},
        #{"value": "from:sakuramiko35", "tag": "Miko"},
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
            profile_image_url = json_response["includes"]["users"][0]["profile_image_url"]
            tweet_user_id = json_response["includes"]["users"][0]["username"]
            matching_rules = json_response["matching_rules"][0]["tag"]

            print(matching_rules)
            print(users_name)
            #print(profile_image_url)
            #print(tweet_user_id)
            #print(tweet_id)

            tweetlink = "https://twitter.com/{}/status/{}"
            tweetlink_content = tweetlink.format(tweet_user_id, tweet_id)

            print(tweetlink_content)

            # Discord Webhooks処理
            main_content = {
                "username": users_name,
                "avatar_url": profile_image_url,
                "content": tweetlink_content
            }
            requests.post(webhook_url_35P_tweet, main_content)

            #print(json.dumps(json_response, indent=4, sort_keys=True))
            tweet = json.dumps(json_response, ensure_ascii=False, indent=4, sort_keys=True)
            tdata = open("tweet-data/tweet.json", "a")
            tdata.write(tweet + ",\n")
            tdata.flush()
            tdata.close()
            print("json出力ok")


def main():
    bearer_token = os.environ.get("BEARER_TOKEN")
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token)
    get_stream(headers, set, bearer_token)


if __name__ == "__main__":
    main()