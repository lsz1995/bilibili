#

import requests
import re
import os
import sys
import json
from lxml import etree
import time
import math

# B站API详情 https://github.com/Vespa314/bilibili-api/blob/master/api.md
head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
}
# 视频AV号列表
aid_list = []

# 评论用户及其信息
info_list = []
infos =[]

# 获取指定UP的所有视频的AV号 mid:用户编号 size:单次拉取数目 page:页数
def getAllAVList(mid, size, page):
    # 获取UP主视频列表
    #for n in range(1,page+1):
     #   url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + \
    #        str(mid) + "&pagesize=" + str(size) + "&page=" + str(n)

        url='https://space.bilibili.com/ajax/member/getSubmitVideos?mid=1739936&page=1&pagesize=25'#up主视频列表
        r = requests.get(url)
        text = r.text
        json_text = json.loads(text)
        # 遍历JSON格式信息，获取视频aid
        for item in json_text["data"]["vlist"]:

            info = {'id':item['aid'],'title':item['title']}
            infos.append(info)
        print(infos)
        print(len(infos))

# 获取一个AV号视频下所有评论
def getAllCommentList(item):

            url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn=1&type=1&oid={}&sort=0'.format(str(int(item)))
            print(url)
            req = requests.get(url)
            text = req.text
            json_text_list = json.loads(text)
            count = json_text_list["data"]["page"]["count"]
            print('总评论',count)
            page = math.ceil(int(count)/20)
            print(page)
            info_list=[]


            for i in range(page):
                url = 'https://api.bilibili.com/x/v2/reply?&jsonp=jsonp&pn={}&type=1&oid={}&sort=0'.format(str(i+1),str(item))#第一，二页
                print(url)

                req = requests.get(url)
                text = req.text
                json_text_list = json.loads(text)
                for i in json_text_list["data"]["replies"]:
                    info_list.append([i["member"]["uname"],i["content"]["message"]])
                print(info_list)
                print(len(info_list))


def getdanmu(ids):#获取一个视频里的弹幕



    url = 'http://bilibili.com/video/av{}'.format(str(ids))
    print(url)
    html = requests.get(url, headers=head)
    #print(html.text)

    cids = re.findall(r'cid=(\d+)&aid', html.text)[0]
    danmu_url = 'https://comment.bilibili.com/{}.xml'.format(cids)
    print(danmu_url)
    comment_text = requests.get(danmu_url, headers=head)
    comment_selector = etree.HTML(comment_text.content)
    comment_content = comment_selector.xpath('//i')
    for comment_each in comment_content:
        comments = comment_each.xpath('//d/text()')
        times =comment_each.xpath('//d/@p')
        for comment in zip(comments,times):
            time=re.split('[,]',comment[1])[4]
            time=timestamp_datetime(int(time))

            print(time,comment[0])











# 保存评论文件为txt
def saveTxt(filename,filecontent):
    filename = str(filename) + ".txt"
    for content in filecontent:
        with open(filename, "a", encoding='utf-8') as txt:
            txt.write(content[0] +' '+content[1].replace('\n','') + '\n\n')
        print("文件写入中")

def timestamp_datetime(value):#unix 时间转换
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

if __name__ == "__main__":
    # 爬取逆风笑 只爬取第一页的第一个
    #getAllAVList(2019740,25,1)#爬取UP主下的所有视频
    getAllCommentList(23263757)#爬取视频下的所有评论#
    #getdanmu(5878692)#

    #for item in aid_list:
    #    info_list.clear()
        #getAllCommentList(item)
    #    saveTxt(item,info_list)