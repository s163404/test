#coding: utf-8

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

numb_key = 9   # twitter api のoauth認証(set_Oauth)に関する情報の 配列番号
numb_split = 10  #  収集データを並列的に収集可能にするため、この指定数で分割し、numb_keyの部分だけを収集する
#filename = "extra20180710.txt"
filename = "followerlist_20180710.txt"  # 入力ファイル
output_filename = "followerlist_20180710-"+str(numb_key)+".txt" # 出力ファイル

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
                retweeters = twitter.get_retweeters_ids(id=tweet['id'], cursor=-1, count = 100)
                print(retweeters)
            except TwythonRateLimitError:
                twitter = set_Oauth(numb_key)
                time.sleep(60 * 15)
                continue
            except StopIteration:
                break
            break

    return retweeter_ids

def get_follower_ids(user_id):
    array_followers_ids = []
    twitter1 = set_Oauth(numb_key)
    followers = ""
    array_followers = []
    while True:
        try:
            followers = twitter1.get_followers_ids(id=user_id)  # or just () - followers for your account
        except TwythonRateLimitError:
            time.sleep(60 * 15)
            twitter1 = set_Oauth(numb_key)
            continue
        except StopIteration:
            print("??")
            break
        except TwythonError:
            print("No user for ID of:", user_id)
            break
        break

    if(followers == ""):
        return ""

    array_followers_ids = followers['ids']
    count = 0
    while True:
        if (followers['next_cursor'] > 0):
            while True:
                try:
                    twitter1 = set_Oauth(numb_key)
                    followers = twitter1.get_followers_ids(id=user_id, cursor=followers[
                        'next_cursor'])  # or just () - followers for your account
                    array_followers_ids.extend(followers['ids'])
                except TwythonRateLimitError:
                    time.sleep(60 * 15 + 10)
                    continue
                except StopIteration:
                    break
                count += 1
                break
        else:
            break

    return array_followers_ids

def read_file(filename, start_rate, end_rate):
    array_userid = []
    f = open(filename)
    data = f.read()
    f.close()
    array_lines = []
    array_lines_tmp = data.split('\n')
    count = 0
    for alt in array_lines_tmp:
        if start_rate*len(array_lines_tmp) <= count < end_rate*len(array_lines_tmp):
            array_lines.append(alt)
        count+=1
    return array_lines

def read_file1(filename):
    array_userid = []
    f = open(filename)
    data = f.read()
    f.close()
    array_lines = data.split('\n')

    for al in array_lines:
        al_tmp = al.split("\t")
        if( len(al_tmp)>1):
            print(al_tmp[0])
            array_lines.append(al_tmp[0])
    return array_lines

def save_data(filename,data):
    f = open(filename, 'a')  # 書き込みモードで開く
    f.write(data+"\n")  # シーケンスが引数。
    f.close()


array_userid = read_file(filename, numb_key/numb_split, (numb_key+1)/numb_split)
array_followerid_fin = read_file1(output_filename)

print("complete reading")
count =0
for au in array_userid:
    followers_tmp = ""
    array_data = []

    count+=1
    if au in array_followerid_fin:
        print(str(count)+"\tOK\t"+str(au))
        continue

    array_followers = get_follower_ids(au)

    for af in array_followers:
        if followers_tmp is "":
            followers_tmp = str(af)
        else:
            followers_tmp = followers_tmp + ","+str(af)
    print(str(numb_key)+"\t"+str(au)+"\t"+followers_tmp)

    save_data(output_filename,str(au)+"\t"+followers_tmp)

sys.exit()
