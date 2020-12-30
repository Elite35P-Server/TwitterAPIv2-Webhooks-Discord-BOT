import requests
import datetime
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='AAAAAAAAAAAAAAAAAAAAAJFEKgEAAAAAUmp%2F8yloASSlyjrrRbV%2BYu3MBE0%3DvHDl6YnmRYk7tx6LIjDjBknIDzUtB48lafGXGwku12qdTvbspH'


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
        {"value": "(#さくらみこ OR #みこなま OR #みこらじお OR #さくら組料理部 OR #みこきいたぞ OR #バブライブ OR #さくらみこ新3Dお披露目 OR #さくらみこMMD) (-is:retweet -is:quote)", "tag": "35P-Tweet"},
        {"value": "(#miko_Art OR #ミコミコ動画 OR #さくらみこMMD) (has:media -is:retweet -is:quote)", "tag": "35P-Art"},
        {"value": "from:sakuramiko35", "tag": "Miko"},
        {"value": "from:ipms_IA -is:retweet", "tag": "test"},
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
            
            # 辞書データから所望の値を取り出す、、、、取り出したい、、、わからん
            matching_rules = json_response["matching_rules"][1]
            tweet_user_name = json_response['includes']['users']['name']
            profile_image_url = json_response['includes']['users']['profile_image_url']
            tweet_user_id = json_response['includes']['users']['username']
            tweet_id = json_response['data']['id']

            print(matching_rules + "/n" + tweet_user_name + "/n" + profile_image_url + "/n" + tweet_user_id + "/n" + tweet_id)

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