import requests
import datetime
import os
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
        time.sleep(120)
        main()
        
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
        
    #count = 0
    for response_line in response.iter_lines():
        if response_line:

            #count += 1
            #if count==5:
            #    count = 0
            #print(count)

            json_response = json.loads(response_line)
            
            # 辞書データから所望の値を取り出す
            tweet_id = json_response["data"]["id"]
            users_name = json_response["includes"]["users"][0]["name"]
            profile_image_url = json_response["includes"]["users"][0]["profile_image_url"].replace("_normal", "")
            tweet_user_id = json_response["includes"]["users"][0]["username"]
            matching_rules = json_response.get("matching_rules")
            matching_rules_tag = [d.get('tag') for d in matching_rules]
            #matching_rules_test1 = matching_rules[0]
            #matching_rules_test2 = matching_rules.get(1)
            #matching_rules_tag = matching_rules.get("tag")

            print(matching_rules_tag)
            #print(matching_rules_test2)
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


            # Discord Webhooks 処理1
            #if count==0:
                #print(tweetlink_content)
                # Discord Webhooks POST
                #requests.post(webhook_url_35P_1, main_content)
                
            # Discord Webhooks 処理2
            #if count==1:
                #print(tweetlink_content)
                # Discord Webhooks POST
                #requests.post(webhook_url_35P_2, main_content)
                
            # Discord Webhooks 処理3
            #if count==2:
                #print(tweetlink_content)
                # Discord Webhooks POST
                #requests.post(webhook_url_35P_3, main_content)
                
            # Discord Webhooks 処理4
            #if count==3:
                #print(tweetlink_content)
                # Discord Webhooks POST
                #requests.post(webhook_url_35P_4, main_content)
                
            # Discord Webhooks 処理5
            #if count==4:
                #print(tweetlink_content)
                # Discord Webhooks POST
                #requests.post(webhook_url_35P_5, main_content)
                
            #print(json.dumps(json_response, indent=4, sort_keys=True))
            tweet = json.dumps(json_response, ensure_ascii=False, indent=4, sort_keys=True)
            tdata = open("tweet.json", "w")
            tdata.write(tweet)
            tdata.flush()
            tdata.close()
            print("json出力ok")
            

def main():
    bearer_token = config.token
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token)
    get_stream(headers, set, bearer_token)


if __name__ == "__main__":
    main()
