#-*-coding:utf8-*-
#代码由MetaMiku改编自https://zhuanlan.zhihu.com/p/498425181?utm_id=0 
#纪念吹哨人李文亮医生

from datetime import datetime ,timedelta    #时间
from hashlib import sha256
from requests_html import HTMLSession       #pip install
from retrying import retry                  #pip install
import re
import urllib3                              # 解除警告
import time
from threading import Thread
urllib3.disable_warnings()
session = HTMLSession()

CommentsList=[]
ID=0
MaxNum=128
zone=+8
MAXRETRIES=128

def init():
    readID = 0
    file = open((datetime.now()+timedelta(hours=zone)).strftime('%Y%m%d')+'.txt',mode = 'a+',encoding='gb18030')
    file.close()
    file = None
    file = open((datetime.now()+timedelta(hours=zone)).strftime('%Y%m%d')+'.txt',mode = 'r',encoding='gb18030')
    for i in file.readlines():
        readID += 1
        checkstring = ''.join(re.findall('^.+\t',i))
        print('[READ'+str(readID)+']'+i,end='')
        check=sha256(checkstring.encode("utf-8")).hexdigest().encode("utf-8")
        CommentsList.append(check)
    while len(CommentsList) > MaxNum:   #过长检测，避免保存过多数据
        CommentsList.pop(0)
    file.close()

def ListAdd(string,check,filename):
    global CommentsList
    global ID
    global MaxNum
    ifexisted=0
    for i in reversed(CommentsList):    #检查是否重复
        if i == check:
            ifexisted = 1
    if ifexisted == 0:                  #非重复，打印日志并写入txt
        ID += 1
        file = None    #清空文件指针
        file = open(filename,mode = 'a+',encoding='gb18030')
        print('[INFO'+str(ID)+'] '+string)
        CommentsList.append(check)
        file.write(string+'\n')
        file.close()
    while len(CommentsList) > MaxNum:   #过长检测，避免保存过多数据
        CommentsList.pop(0)
    return 0

def getresponse():
    user_url = 'https://weibo.com/1139098205/Is9M7taaY#comment' #目标微博地址，剩下的基本上照搬过来的，再次感谢https://zhuanlan.zhihu.com/p/498425181?utm_id=0
    cookie = ''
    headers_1 = {
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
    }
    uid_1 = re.findall('/(.*?)#', user_url)[0]
    uid_2 = uid_1.split('/', 3)[3]
    url_1 = f'https://weibo.com/ajax/statuses/show?id={uid_2}'
    response = session.get(url_1, proxies={'http': '', 'https': ''}, headers=headers_1, verify=False).content.decode()
    weibo_id = re.findall('"id":(.*?),"idstr"', response)[0]
    start_url = f'https://m.weibo.cn/comments/hotflow?id={weibo_id}&mid={weibo_id}&max_id_type=0'
    response = session.get(start_url, proxies={'http': '', 'https': ''}, headers=headers_1, verify=False).json()
    return response

def main():
    response = getresponse()
    data_list = response['data']['data']
    for data_json_dict in reversed(data_list):
        #提取评论内容
        try:
            texts_1 = data_json_dict['text']
                #需要替换的内容, 替换之后的内容, 替换对象
            alts = ''.join(re.findall(r'alt=(.*?) ', texts_1))
            texts = re.sub("<span.*?</span>", alts, texts_1)        #评论文本
            #like_counts = str(data_json_dict['like_count'])        #点赞量
            created_at = data_json_dict['created_at']               #评论时间   格林威治时间---需要转化为北京时间
            std_transfer = '%a %b %d %H:%M:%S %z %Y'
            std_create_times = str(datetime.strptime(created_at, std_transfer))[0:19]
            gender = data_json_dict['user']['gender']
            genders = '女' if gender == 'f' else '男'               #性别 女f男m
            screen_names = data_json_dict['user']['screen_name']    #用户名
            IPsource = data_json_dict['source']                     #IP属地
            
            string = screen_names +'\t'+ genders +'\t'+ std_create_times +'\t'+ IPsource +'\t'+ texts
            checkstring = screen_names +'\t'+ genders +'\t'+ std_create_times +'\t'+ IPsource +'\t'
            check = sha256(checkstring.encode("utf-8")).hexdigest().encode("utf-8")
            filename = std_create_times[0:4] + std_create_times[5:7] + std_create_times[8:10] +'.txt'
            ListAdd(string,check,filename)
        except Exception as e:
            print('[WARN]'+str(e))
            continue

if __name__ == '__main__':
    init()
    print('[INFO0]init finished. main started.')
    while 1:
        try:
            Thread(target=main).start()
        except Exception as e:
            print('[ERROR]'+str(e))
        time.sleep(60)
