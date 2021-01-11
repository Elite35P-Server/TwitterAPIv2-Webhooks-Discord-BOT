import requests
import datetime
import os
import json
import time

from dotenv import load_dotenv
load_dotenv()

webhook_url_35P_1 = os.getenv("35P_1")
webhook_url_35P_2 = os.getenv("35P_2")
webhook_url_35P_3 = os.getenv("35P_3")
webhook_url_35P_4 = os.getenv("35P_4")
webhook_url_35P_5 = os.getenv("35P_5")
webhook_url_35P_Art = os.getenv("35P_Art")
webhook_url_Admin_twitter = os.getenv("Admin_twitter")

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
        {"value": "(#さくらみこ OR さくらみこ OR #miko_Art OR #みこなま OR #ミコミコ動画 OR #みこらじお OR #さくら組料理部 OR #みこきいたぞ OR #バブライブ OR #みっころね OR ぺこみこ OR #桃鉄みみおる OR #さくらみこ新3Dお披露目 OR #さくらみこMMD OR #35P OR #みこぴー OR #さくら色Dreamer OR #35PProject) (-is:retweet)", "tag": "35P-Tweet"},
        #{"value": "(#ホロお正月CUP OR #ゆくホロくるホロ2020 OR #ホロライブ正月衣装) (-is:retweet)", "tag": "holo-2021"},
        {"value": "(#ホロお正月CUP) (-is:retweet)", "tag": "holo-2021"},
        {"value": "(#miko_Art OR #ミコミコ動画 OR #さくらみこMMD) (has:media -is:retweet -is:quote)", "tag": "35P-Art"},
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
    count = 0

    for response_line in response.iter_lines():
        if response_line:

            count += 1
            if count==5:
                count = 0
            print(count)

            json_response = json.loads(response_line)

            # 辞書データから所望の値を取り出す
            tweet_id = json_response["data"]["id"]
            users_name = json_response["includes"]["users"][0]["name"]
            profile_image_url = json_response["includes"]["users"][0]["profile_image_url"]
            tweet_user_id = json_response["includes"]["users"][0]["username"]
            matching_rules = json_response.get("matching_rules")
            matching_rules_test1 = matching_rules[0]
            #matching_rules_test2 = matching_rules.get(1)
            #matching_rules_tag = matching_rules.get("tag")

            print(matching_rules)
            #print(matching_rules_test2)
            print(users_name)
            #print(profile_image_url)
            #print(tweet_user_id)
            #print(tweet_id)

            tweetlink = "https://twitter.com/{}/status/{}"
            tweetlink_content = tweetlink.format(tweet_user_id, tweet_id)

            main_content = {
                  "username": users_name,
                   "avatar_url": profile_image_url,
                  "content": tweetlink_content
            }

            #time.sleep(0.1)
            # Discord Webhooks 処理1
            if count==0:
                print(tweetlink_content)
                # Discord Webhooks POST
                requests.post(webhook_url_35P_1, main_content)
                
            # Discord Webhooks 処理2
            if count==1:
                print(tweetlink_content)
                # Discord Webhooks POST
                requests.post(webhook_url_35P_2, main_content)
                
            # Discord Webhooks 処理3
            if count==2:
                print(tweetlink_content)
                # Discord Webhooks POST
                requests.post(webhook_url_35P_3, main_content)
                
            # Discord Webhooks 処理4
            if count==3:
                print(tweetlink_content)
                # Discord Webhooks POST
                requests.post(webhook_url_35P_4, main_content)
                
            # Discord Webhooks 処理5
            if count==4:
                print(tweetlink_content)
                # Discord Webhooks POST
                requests.post(webhook_url_35P_5, main_content)
                
            #print(json.dumps(json_response, indent=4, sort_keys=True))
            tweet = json.dumps(json_response, ensure_ascii=False, indent=4, sort_keys=True)
            tdata = open("tweet-data/tweet.json", "w")
            tdata.write(tweet)
            tdata.flush()
            tdata.close()
            print("json出力ok")
            

def main():
    bearer_token = os.getenv("BEARER_TOKEN")
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token)
    get_stream(headers, set, bearer_token)


if __name__ == "__main__":
    main()
