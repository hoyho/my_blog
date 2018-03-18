#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import random
import hashlib

import requests
import json
import os
import base64
from Crypto.Cipher import AES
from pprint import pprint
import binascii
import MySQLdb
import sys
import threading
import datetime,time
import logging
import random

import queue as queue
import pdb
from urllib.error import HTTPError

#本程序使用了两个API
#（1）获取歌曲描述:http://music.163.com/api/song/detail/?id=%s&ids=[%s]
#（2）获取歌曲评论：http://music.163.com/weapi/v1/resource/comments/R_SO_4_30953009/?csrf_token=???


logging.basicConfig(level=logging.ERROR,format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s |  %(message)s',
                datefmt='%H:%M:%S',
                filename='crawler-%s.log'%str(datetime.date.today()),
                filemode='a')

queue = queue.Queue()# 创建一个队列

#logging.basicConfig(filename='./log'+str(datetime.date.today())+'.txt', level=logging.DEBUG)


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext).decode('u8')
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    #print ('text:'+str(text))
    #rs = int(codecs.encode(str(text),"hex"), 16)**int(pubKey, 16) % int(modulus, 16)
    #rs = int(str(text).encode('hex'), 16) ** int(pubKey, 16) % int(modulus, 16)
    rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16)) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


def createSecretKey(size):
    return binascii.hexlify(os.urandom(size))[:16]
    #return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16]


# 歌曲加密算法, 基于https://github.com/yanunon/NeteaseCloudMusic脚本实现
def encrypted_id(id):
    magic = bytearray('3go8&$8*3*3h0k(2)2', 'u8')
    song_id = bytearray(id, 'u8')
    magic_len = len(magic)
    for i, sid in enumerate(song_id):
        song_id[i] = sid ^ magic[i % magic_len]
    m = hashlib.md5(song_id)
    result = m.digest()
    result = base64.b64encode(result)
    result = result.replace(b'/', b'_')
    result = result.replace(b'+', b'-')
    return result.decode('u8')


# 获取高品质mp3 url #songId $ songName $ artist $ downLoadUrl $ quality
def GetSongInfo(song):
    print("GetSongInfo...")
    quality = 0
    songId=0
    songName='unknow'
    artist='unknow'
    try:

        # print(song['songs'])
        if not  song['songs']:
            print('song not exist')
            return 'unknow$unknow$unknow$unknow$unknow'
        for item in song['songs']:
            # 获取歌名，id，歌手
            if item['name']:
                # print('songname:\n'+item['name'])
                songName = item['name']

            if item['id']:
                # print('@@@id:\n' + str(item['id']))
                songId = str(item['id'])

            if item['artists']:
                for info in item['artists']:
                    if info['name']:
                        # print('@@@singername:\n'+info['name'])
                        artist = info['name']
            # 获取下载/播放url
            if item['hMusic'] and quality <= 0:
                music = item['hMusic']
                quality = 'HD'
            elif item['mMusic'] and quality <= 1:
                music = item['mMusic']
                quality = 'MD'
            elif item['lMusic'] and quality <= 2:
                music = item['lMusic']
                quality = 'LD'
            else:
                print('#unknow else quality , no copyright???')
                return songId + '$' + songName + '$' + artist + '$' + 'unknow' + '$' + 'unknow quality'

            quality = quality + ' {0}k'.format(music['bitrate'] // 1000)
            # print('quality:'+str(quality))
            song_id = str(music['dfsId'])
            enc_id = encrypted_id(song_id)
            # print(str(enc_id))
            downLoadUrl = 'http://m%s.music.126.net/%s/%s.mp3' % (random.randrange(1, 3),
                                                                  enc_id, song_id)
            return songId + '$' + songName + '$' + artist + '$' + downLoadUrl + '$' + quality  # songId $ songName $ artist $ downLoadUrl $ quality

        return 'unknow$unknow$unknow$unknow$unknow'
    except Exception as e:
        print(e)
        print('can''t get url')


# 获取歌曲评论
# 相关http://music.163.com/weapi/v1/resource/comments/R_SO_4_30953009/?csrf_token=
def GetSongComment(songid,ip,isUseProxy):
    print("GetSongComment...")
    commentUrl = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_%s/?csrf_token=' % songid
    headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/'
    }
    userInfo = {
        'username': 'rome1qaz@163.com',
        'password': 'password',
        'rememberLogin': 'true'
    }
    modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
               'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
               '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
               '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
               '3ece0462db0a22b8e7')
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'
    userInfo = json.dumps(userInfo)
    secKey = createSecretKey(16)
    #encText = aesEncrypt(aesEncrypt(userInfo, nonce), secKey)
    #encSecKey = rsaEncrypt(secKey, pubKey, modulus) #耗时，直接指定,注意时效，定期更换
    encText='FVs+pswBzqmg6QVXubE48YeEDvWqcQSsWOdxWVVe7rxoWX3uhVRVsFUX6qdc9XiwZ7LnhHeEnwlolGDVviiKVYMaWS99ScyggcGeRamUG8LC2hnGskOgtlp1/LxCYezlYhWvF4pSqg1t7i+aEaLBiw=='
    encSecKey='421c340017432f396c87f1bebc121a314125f929cfcf0ed407b770f0da4beb8795a7b8951035b3c47b22215823aeeedce52bdf4acfda47263263dd646cfe8f7a623ba3c4a323b31357daaca4a74174761905ea173ed1a130f53d99238576973c7f6271b15bffd054fa10381a570d31e27e37d74201045e2a11a86c2b9e54776f'
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }

    http_proxy = "http://" +ip
    https_proxy = "https://"+ip
    #ftp_proxy = "ftp://10.10.1.10:3128"
    proxyDict = {
        "http": http_proxy,
        "https": https_proxy
        #"ftp": ftp_proxy
    }

    for tryTime in range(3):
        try:
            if isUseProxy:
                print('current proxy:' + http_proxy)
                req_response = requests.post(commentUrl, headers=headers, data=data, proxies=proxyDict, timeout=30)
            else:
                req_response = requests.post(commentUrl, headers=headers, data=data, timeout=30)

            if req_response.status_code != 200:
                logging.error("return code:" + str(req_response.status_code))
                logging.error("bad url,please check you url  " + commentUrl)
                print("!!!!!!!!!!!!!!!!!!!!! " + "status code:" + str(
                    req_response.status_code) + " songid:" + songid + '\n exit thread\n')
                if tryTime == 3:
                    exit()
            else:
                return ResolveComment(req_response)  # mycommentInfo, commetCount
        except Exception as e:
            print(e)
            logging.error(e)






#解析评论json内容,返回歌曲信息字典，和总评论数
# 评论用户，赞，评论内容 + 总评论数
'''
commentInfo=
[
 {'user':'' , 'like':'' , 'content':''},
 {'user':'' , 'like':'' , 'content':''},
 {'user':'' , 'like':'' , 'content':''},
 ...
]
'''
def ResolveComment(response):
    commentInfo=[]
    try:
        print('total comment count:'+str(response.json()['total']))
    except Exception as e:
        print("eeeeeeeeeeeeeeeeeeee\n" + "response:" + str(response.status_code) +str(response.json()))
        print(e)

        #print(response.json())
    commentCount=str(response.json()['total'])
    #pprint(response.json())
    print(' \n--------------\n')
    i=0
    if response.json()['hotComments']:
        print("hot comments:\n")
        for comment in response.json()['hotComments']:
            if i<10:
                commentInfo.append({'user': '', 'content': '', 'like': ''})
                if comment['beReplied']:  # 热评是回复别人
                    print(comment['user']['nickname'])
                    print('like:' + str(comment['likedCount']))
                    print(comment['content'])
                    print('\n\n')
                    commentInfo[i]['like'] = str(comment['likedCount'])
                    commentInfo[i]['content'] = comment['content']
                    commentInfo[i]['user'] = comment['user']['nickname']
                    for bereplied in comment['beReplied']:
                        print('-----\n' + bereplied['content'])
                        print('-----\t')
                else:
                    print(comment['user']['nickname'])
                    print('like:' + str(comment['likedCount']) )
                    print(comment['content'])
                    commentInfo[i]['user'] = comment['user']['nickname']
                    print('\n\n')
                    commentInfo[i]['like'] = str(comment['likedCount'])
                    commentInfo[i]['content'] = comment['content']

                i=i+1
            else:
                break
    return commentInfo,commentCount

'''
commentInfo=
[
 {'user':'' , 'like':'' , 'content':''},
 {'user':'' , 'like':'' , 'content':''},
 {'user':'' , 'like':'' , 'content':''},
 ...
]
'''


def log(text):
    filename=str(datetime.date)+'.log'
    #todo


#获取歌曲基本信息，返回json
#API(1) http://music.163.com/api/song/detail/?id=%s&ids=[%s]
def GetSongDescription(id,ip,isUseProxy):
    targetUrl = 'http://music.163.com/api/song/detail/?id=%s&ids=[%s]' % (id, id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
    }

    http_proxy = "http://" +ip
    https_proxy = "https://"+ip
    #ftp_proxy = "ftp://10.10.1.10:3128"
    proxyDict = {
        "http": http_proxy,
        "https": https_proxy
        #"ftp": ftp_proxy
    }
    #requests.get(url, headers=headers, proxies=proxyDict)
    try:
        if isUseProxy:
            songDetail = requests.get(targetUrl, headers, proxies=proxyDict, timeout=30).text
        else:
            songDetail = requests.get(targetUrl, headers, timeout=30).text
        jsondData = json.loads(songDetail)
        return jsondData
    except HTTPError as err:
        if err.code == 404:
            logging.error("Error: %s, reason: %s." % (err.code, err.reason))
            print("Error: %s, reason: %s." % (err.code, err.reason))
            exit()
    except:
        try:
            songDetail = requests.get(targetUrl, headers, timeout=18).text
            jsondData = json.loads(songDetail)
            return jsondData
        except Exception as e:
            print(e)
            print("exit error thread")
            exit()
    # print("songDetail:")



#执行一句或者多句sql命令
def ExecuteDb(sqls):
    try:
        conn = MySQLdb.connect(host='139.59.xxx.xxx', user='user', passwd='psw', port=3306,charset='utf8')
        cursor = conn.cursor()
        # SQL 查询语句，需要单独执行
        for cmd in sqls.split(';'):
            if len(cmd)>0:
                #u = u'%s'%cmd
                #cmd=u.encode('latin-1', 'ignore')
                cursor.execute(cmd)
                conn.commit()

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(e)
        logging.error(e)
        return False


def SendMail(to_account, subject, content):
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    from_account='rome1qaz@163.com'
    from_passwd='password'
    SMTP_host='smtp.163.com'
    # create msg
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')  # subject
    msg['From'] = from_account
    msg['To'] = to_account
    try:
        email_client = smtplib.SMTP(SMTP_host)
        email_client.login(from_account, from_passwd)
        email_client.sendmail(from_account, to_account, msg.as_string())
        print("邮件发送成功")
        email_client.quit()
    except Exception as e:
        logging.error(e)
        print("Error: 无法发送邮件")
        print(e)



def C(info):
    #pdb.set_trace()
    print('cccc'+str(info))


def GetIPlist():
    ipList=[]
    try:
        print('get ip from ip.txt')
        with open('ip.txt', 'rt') as f:
            for line in f:
                ipList.append(line)
    except Exception as e:
        logging.error(e)
    return ipList

#从队列中获取数据生成多句sql
def GenerateSQL(queue_list,trytime):

    combineStrs=''
    for threadResult in queue_list:
        if threadResult['songPage']:
            songPage=str(threadResult['songPage'])

        if threadResult['songInfoList']:
            songId = int(threadResult['songId'])
            songName =threadResult['songInfoList'][1]
            artist =threadResult['songInfoList'][2]
            downLoadUrl = threadResult['songInfoList'][3]
            quality = threadResult['songInfoList'][4]
            if songName =='unknow' and artist=='unknow' and downLoadUrl=='unknow':
                isValidSong =False
                next
            else:
                isValidSong =True


        if threadResult['commentDict']:
            commentDict=threadResult['commentDict']
            if len(commentDict)>0:
                commentPart=""
                for comment in commentDict:
                    #commentPart="'" + comment['user']+"'" +',' + "'"+ comment['like'] +"'" +','+ "'" + comment['content'] +"'" + ","
                    commentPart = commentPart + "'" + comment['user'].replace("'", "''") + "'" + ',' + "'" + comment['content'].replace("'", "''") + "'" + ','  + comment['like'].replace("'", "''")  + ","
                    if comment['user']:
                        user1=comment['user']
                    if comment['like']:
                        like1=comment['like']
                    if comment['content']:
                        content1=comment['content']
                if commentPart.endswith(','):
                    commentPart = commentPart[:-1]
                if len(commentDict) <10:
                    for left in range(10-len(commentDict)):
                        commentPart = commentPart + ",'' " + ",'' " + ",0 "
        else:
            'commentPart is null'
            commentPart=" '','',0,'','',0,'','',0,'','',0,'','',0,'','',0,'','',0,'','',0,'','',0,'','',0 "
        #把‘或者“ 替换成中文引号”，避免数据库字符冲突
        songName = songName.replace("'","”").replace('"','”')
        artist.replace("'","”").replace('"','”')
        commentPart.replace("'","”").replace('"','”')
        if threadResult['commentCount'] and isValidSong:
            commentCount = int(threadResult['commentCount'])
            partA = 'INSERT INTO netease.musicInfo (songName,singer,songPage,songSrc,commentCount,songId,tryTime,quality,user1,' \
                         'comment1,likeCount1,user2,comment2,likeCount2,user3,comment3,likeCount3,user4,comment4,likeCount4,' \
                         'user5,comment5,likeCount5,user6,comment6,likeCount6,user7,comment7,likeCount7,user8,comment8,likeCount8,' \
                         'user9,comment9,likeCount9,user10,comment10,likeCount10)'
            partB = 'values("%s","%s","%s","%s",%d,%d,%d,"%s"' %(songName,artist,songPage,downLoadUrl,commentCount,songId,trytime,quality) + ","+ commentPart + ')'
            sql =partA+partB +";"
            '''
                        insertSingle='INSERT INTO netease.musicInfo(songName,singer,songPage,songSrc,commentCount,user1,' \
                         'comment1,likeCount1,user2,comment2,likeCount2,user3,comment3,likeCount3,user4,comment4,likeCount4,' \
                         'user5,comment5,likeCount5,user6,comment6,likeCount6,user7,comment7,likeCount7,user8,comment8,likeCount8,' \
                         'user9,comment9,likeCount9,user10,comment10,likeCount10' \
                         ')values("%s","%s","%s","%s",%d, '%(songName,artist,songPage,downLoadUrl,commentCount) + commentPart+')'
            '''

            combineStrs = combineStrs +sql
    return  combineStrs

# 线程执行任务
def ThreadWork(inSongId,inSongIp,isUseProxy):
    threadSongId=inSongId #线程间不用占用songid
    songPage = 'http://music.163.com/#/song?id=' + threadSongId
    songBasicJson = GetSongDescription(threadSongId,inSongIp,isUseProxy)


    infoStrs = GetSongInfo(songBasicJson)
    try:
        if not infoStrs: #无版权等原因获取不到信息，返回tuple
            infoStrs='unknow$unknow$unknow$unknow$unknow'
        if infoStrs!='unknow$unknow$unknow$unknow$unknow':
            songInfoList = infoStrs.split('$')  ##songId $ songName $ artist $ downLoadUrl $ quality
            commentDict, commetCount = GetSongComment(threadSongId, inSongIp, isUseProxy)
            threadResult = {'songPage': songPage,
                            'songInfoList': songInfoList,
                            'commentDict': commentDict,
                            'commentCount': commetCount,
                            'songId': threadSongId
                            }
            queue.put(threadResult)
        else:
            print('end GetSongComment')
    except Exception as e:
        logging.error(e)
        logging.error('infoStrs:'+str(infoStrs))
        print(infoStrs)

    #print('completed songid=' + songid)



def Dispatch2():
    starttime = datetime.datetime.now()
    ipList=[]
    isUseProxy =False
    while True:
        #read proc
        try:

            conn = MySQLdb.connect(host='139.59.xxx.xxx', user='user', passwd='psw', port=3306,db='netease')
            cursor = conn.cursor()
            # SQL 查询语句
            cursor.callproc('CreateTaskRecord')
            #scursor.execute('call CreateTaskRecord();')
            data = cursor.fetchall()
            cursor.close() #避免执行conn.commit()时候出现commands out of sync you can't run this command now
            cursor = conn.cursor()
            conn.commit() #只有commit后存储过程中的insert语句才会生效
            representId = data[0][0]
            initBatID =data[0][1]
        except Exception as e:
            print(e)
            print('error')
            logging.error(e)
            SendMail('hoyho@foxmail.com','mysql error',str(e))
            print('continute...')
            continue
        finally:
            cursor.close()
            conn.close()


        tryTime =1
        initFlag = False


        for trying in range(5):
            # update IPlist
            nowtime = datetime.datetime.now()
            Timediff = (nowtime - starttime).seconds
            if (Timediff > 300 or initFlag == False) and isUseProxy:
                print('update iplist')
                try:
                    with open('ip.txt', 'rt') as f:
                        for line in f:
                            ipList.append(line)
                except Exception as e:
                    logging.error(e)
                starttime = nowtime

            # 0点后更换log文件
            logging.basicConfig(level=logging.ERROR,
                                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s|%(message)s',
                                datefmt='%H:%M:%S',
                                filename='crawler-%s.log' % str(datetime.date.today()),
                                filemode='a')
            # debeug =queue.qsize()

            # start theaad
            threads = []
            for i in range(10):
                if len(ipList) > 0:
                    inIP = random.choice(ipList)[:-1]  # 去除末尾\n
                else:
                    inIP = '127.0.0.1:1080'
                inID = str(representId+i)
                thread = threading.Thread(target=ThreadWork, args=[inID, inIP,isUseProxy])
                # thread = threading.Thread(target=C, args=i)
                thread.start()  # start()表示启动线程
                threads.append(thread)
            for i in range(10):
                threads[i].join()  # join()表示等待至线程终止


            if tryTime < 4:
                print("Read threads status...\n")
                done = False
                while not done:
                    for t in threads:
                        if t.is_alive():
                            done = False
                            break
                        else:
                            done= True
                    if not done:
                        time.sleep(3)
                        continue
                    else:
                        break #跳出线程等待while循环
                qsize = queue.qsize()
                if done == True:
                    if qsize >=0:
                        print("get results from queue..")
                        queue_data = []
                        while not queue.empty():
                            queue_data.append(queue.get())
                        sqls = GenerateSQL(queue_data, tryTime)
                        if ExecuteDb(sqls):
                            #updateStatus = "INSERT INTO netease.schedule(batchID,representId,tryTime,status,lastUpdateDate)values(%d,%d,%d,'%s',NOW())"%(initBatID,representId,tryTime,"completed")
                            updateStatus = "UPDATE netease.schedule SET tryTime=%d, status ='%s',lastUpdateDate=NOW() WHERE batchID=%d AND  representId =%d"%(tryTime,'completed',initBatID,representId)
                            #print(updateStatus)
                            if ExecuteDb(updateStatus):
                                print("next batch job")
                                break #跳出for trying in range(5):
                            else:
                                print('next batch job')
                                SendMail('hoyho@foxmail.com', 'NetEaseMusic Crawler Fail Report', 'fail ')
                                break #退出for trying in range(5):

                        else: #获取了到音乐信息但没能插入数据库
                            tryTime+=1
                            time.sleep(1)
                            print('sleep for 1 second')
                            continue #for trying in range(5):
                    else:
                        print("qsize < 1 , exit and waiting next check")
                        tryTime = 5  # 直接置５，再试一次
                        continue #for trying in range(5):

                else:
                    print("done 只有false时候才会来到这里，所以理论上不会进这个else")
            else:  # more than 5 time mark as fail task
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                updatefailStatus = "UPDATE netease.schedule SET tryTime=%d, status ='%s',lastUpdateDate=NOW() WHERE batchID=%d AND  representId =%d"%(tryTime,'fail',initBatID,representId)
                print(updatefailStatus)
                if ExecuteDb(updatefailStatus):
                    logging.error(updatefailStatus)
                    print("update fail status done")
                    break  #exit for trying in range(5): enter big while
                else:
                    print("send  notify email")
                    SendMail('hoyho@foxmail.com','NetEaseMusic Crawler Fail Report','')
                    break  #exit for trying in range(5): enter big while
        time.sleep(1)





if __name__ == "__main__":
    print("program begin!!!\n")
    try:
        # SendMail('hoyho@foxmail.com','NetEase Music Crawl Report','hello world sent from debian')
        Dispatch2()
    except Exception as e:
        print(e)
        logging.error(e)
        try:
            SendMail('hoyho@foxmail.com', 'error report' + str(e)[0, 10], str(e))
        except Exception as sendFail:
            logging.error(sendFail)
        raise



