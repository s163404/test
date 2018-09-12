#coding: utf-8

# 特定ユーザIDのツイートに対する、リツイートを収集するプログラム
# 基本的に、検索で収集している。yahooニュースサイトは含めない。また他のサイトの動画サイトを発信しているが含めない
#
# yahoonews:
# tweet id: user id: date: retweet count: favorite count \t tweet text

# retweet:
# tweet id: tweet user id: date \t retweet id: retweet user id: date
import sys

import time
from twython import Twython, TwythonError, TwythonRateLimitError
import re

numb_key = 4   # twitter api のoauth認証(set_Oauth)に関する情報の 配列番号
user_id = 88846085; # yahoonews の user id

pressed = ''
max_id = None

list_tweetid = []
list_newstitle = []
list_newsdata = []
list_retweetdata = []
list_tweetdate = []


def set_Oauth(numb_key):

    CK_array = [
        #  Consumer Key を配列で
    ]

    CS_array = [
        #  Consumer Secret を配列で
    ]

    AT_array = [
        # access token を配列で
    ]

    AS_array = [
        # access token secret を配列で
    ]

    CK = CK_array[numb_key]  # "XXXXXXXXXXXXXXXXXXXXXX" #Consumer key
    CS = CS_array[numb_key]  # "XXXXXXXXXXXXXXXXXXXXXX" #Consumer secret
    AT = AT_array[numb_key]  # "XXXXXXXXXXXXXXXXXXXXXX" #Access token
    AS = AS_array[numb_key]  # "XXXXXXXXXXXXXXXXXXXXXX" #Access token secret

#    client_args = {'proxies': {'http': 'proxy.nagaokaut.ac.jp:8080'}}

    return Twython(CK, CS, AT, AS)
#    return Twython(CK, CS, AT, AS, client_args = client_args)

def save_data(filename, savedata, mode):
 #   try:
    f = open(filename, mode)  # 書き込みモードで開く
    for i in range(len(savedata)-1):
        try:
            f.write(savedata[i].encode("UTF-8"))
        except Exception as e:
            f.write(savedata[i].encode("UTF-8"))
            print(e)
    f.close()

def get_retweeter_ids(user_id):
    twitter = set_Oauth(numb_key)
    retweeter_ids = []
    tweets = twitter.get_user_timeline(user_id=user_id,
                                       count=100,
                                       cursor=-1,
                                       trim_user=True,
                                       exclude_replies=True,
                                       include_rts=False)
    for tweet in tweets:
        print(str(tweet['id']) + ":" + str(tweet['user']['id'])+":"+str(tweet['retweet_count']))

        while True:
            try:
                retweeters = twitter1.get_retweeters_ids(id=tweet['id'], cursor=-1, count = 100)
                print(retweeters)
            except TwythonRateLimitError:
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break
            break

    return retweeter_ids

# ここから、メイン
twitter1 = set_Oauth(numb_key+1)

print(get_retweeter_ids(user_id))

sys.exit()
