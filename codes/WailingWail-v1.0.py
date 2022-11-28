# !/usr/bin/nev python
# -*-coding:utf8-*-
# version 1.0
# 代码由MetaMiku改编自https://zhuanlan.zhihu.com/p/498425181?utm_id=0，为纪念李文亮医生
from datetime import datetime ,timedelta
from hashlib import sha256
from requests_html import HTMLSession
import re, time
import tkinter as tk
import urllib3                      # 解除警告
import time
urllib3.disable_warnings()
session = HTMLSession()

CommentsList=[]
ID=0
MaxNum=64
def ListAdd(string,writein,check):
    global CommentsList
    global ID
    global MaxNum
    ifexisted=0
    for i in reversed(CommentsList):
        if i == check:
            ifexisted = 1
    if ifexisted == 0:
        ID += 1
        print('[INFO'+str(ID)+'] '+string)
        CommentsList.append(check)
        writein.write(string+'\n')
    while len(CommentsList) > MaxNum:
        CommentsList.pop(0)
    return 0
def main():
    user_url = 'https://weibo.com/1139098205/Is9M7taaY#comment'
    pass_wd = ''
    headers_1 = {
        'cookie': pass_wd,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
    }
    headers_2 ={
        "referer": "https://m.weibo.cn/status/Kk9Ft0FIg?jumpfrom=weibocom",
        'cookie': pass_wd,
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36'
    }
    uid_1 = re.findall('/(.*?)#', user_url)[0]
    uid_2 = uid_1.split('/', 3)[3]
    # print(uid_2)
    url_1 = f'https://weibo.com/ajax/statuses/show?id={uid_2}'
    prox = ''
    response = session.get(url_1, proxies={'http': prox, 'https': prox}, headers=headers_1, verify=False).content.decode()
    # print(response)
    weibo_id = re.findall('"id":(.*?),"idstr"', response)[0]
    # print(weibo_id)
    # 构造起始地址
    start_url = f'https://m.weibo.cn/comments/hotflow?id={weibo_id}&mid={weibo_id}&max_id_type=0'
    prox = ''
    response = session.get(start_url, proxies={'http': prox, 'https': prox}, headers=headers_2, verify=False).json()
    data_list = response['data']['data']
    #print(data_list)
    writein=None
    writein = open((datetime.now()+timedelta(hours=+0)).strftime('%Y%m%d')+'.txt',mode = 'a+',encoding='gb18030')
    #print('DEBUGGGGGGG')
    for data_json_dict in reversed(data_list):
        # 提取评论内容
        try:
            #print('HI')
            texts_1 = data_json_dict['text']
            """需要sub替换掉标签内容"""
                # 需要替换的内容, 替换之后的内容, 替换对象
            alts = ''.join(re.findall(r'alt=(.*?) ', texts_1))
            texts = re.sub("<span.*?</span>", alts, texts_1)
            # 点赞量
            like_counts = str(data_json_dict['like_count'])
            # 评论时间   格林威治时间---需要转化为北京时间
            created_at = data_json_dict['created_at']
            std_transfer = '%a %b %d %H:%M:%S %z %Y'
            std_create_times = str(datetime.strptime(created_at, std_transfer))
            gender = data_json_dict['user']['gender']
            genders = '女' if gender == 'f' else '男'
            screen_names = data_json_dict['user']['screen_name']# 用户名
            IPsource = data_json_dict['source']# IP属地
            #print(data_json_dict)
            string=screen_names+'\t'+genders+'\t'+std_create_times+'\t'+IPsource+'\t'+texts
            check=sha256((screen_names+std_create_times).encode("utf-8")).hexdigest().encode("utf-8")
            ListAdd(string,writein,check)
        except Exception as e:
            print('[WARN]'+str(e))
            continue
    writein.close()

if __name__ == '__main__':
    while 1:
        try:
            main()
        except Exception as e:
            print('[ERROR]'+str(e))
        time.sleep(60)
