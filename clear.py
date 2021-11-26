#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import re
import urllib
import requests
from multiprocessing.pool import ThreadPool


def check_url(url):
    headers = {
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.68 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9,zh;q=0.8,und;q=0.7",
    }
    try:
        rs = requests.session()
        res = rs.head(url, headers=headers, timeout=10)
        if 200 <= res.status_code < 400:
            print("检测成功", res.status_code, url)
            return True
    except Exception as e:
        pass
    return False


def get_search_url(SourceUrl, SearchUrl):
    UrlSplit = urllib.parse.urlparse(SearchUrl)
    if SearchUrl is None or UrlSplit.netloc == "":
        return SourceUrl
    else:
        return UrlSplit.scheme + "://" + UrlSplit.netloc


def takeUpdateTime(elem):
    return elem.get("lastUpdateTime", 0)


def sortSource(source_content):
    sort_list = []
    source_content.sort(key=takeUpdateTime, reverse=True)
    i = 1
    for d in source_content:
        d["customOrder"] = i
        sort_list.append(d)
        i = i + 1
    return sort_list


def filter_str(desstr):
    restr = ''
    # 过滤除中英文及数字以外的其他字符
    # res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9|;]")
    # 过滤掉数字
    res1 = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z|;]")
    desstr = res1.sub(restr, desstr)
    res2 = re.compile("[^;]*失效[^;]*")
    desstr = res2.sub(restr, desstr)
    desstr = desstr.replace(';;', ';')
    res3 = re.compile("^;|;$")
    desstr = res3.sub(restr, desstr)

    desstr = desstr.replace('仅发现组', '0仅发现组')
    desstr = desstr.replace('无效组', '0无效组')
    return desstr


def startcheck(d):
    bookSourceGroup = d.get("bookSourceGroup")
    bookSourceUrl = d.get("bookSourceUrl")
    searchUrl = None
    if d.get("ruleSearchUrl") is not None:
        searchUrl = d.get("ruleSearchUrl")
    elif d.get("searchUrl") is not None:
        searchUrl = d.get("searchUrl")

    if bookSourceGroup is not None and "仅发现组" not in bookSourceGroup:
        SourceUrl = get_search_url(bookSourceUrl, searchUrl)
        if not check_url(SourceUrl):
            d["bookSourceGroup"] = "无效组"
    if d.get("bookSourceGroup") is not None:
        d["bookSourceGroup"] = filter_str(d.get("bookSourceGroup"))
    CheckList.append(d)


source_content = []
new_RSS_content = []
SourceList = {}

with open("yuedu_source.json", 'r', encoding='utf-8') as file_to_read:
    resjson = json.loads(file_to_read.read())
    source_content.extend(resjson)

for d in source_content:
    bookSourceName = d.get("bookSourceName")
    bookSourceGroup = d.get("bookSourceGroup")
    bookSourceUrl = d.get("bookSourceUrl")
    searchUrl = None
    if d.get("ruleSearchUrl") is not None:
        searchUrl = d.get("ruleSearchUrl")
    elif d.get("searchUrl") is not None:
        searchUrl = d.get("searchUrl")
    SourceUrl = get_search_url(bookSourceUrl, searchUrl)
    FindFlage = "N"
    SearchFlage = "N"
    OnlyFindFlage = "N"

    if d.get("ruleFindUrl") is not None:
        FindFlage = "Y"
    if d.get("ruleSearchUrl") is not None or d.get("searchUrl") is not None:
        SearchFlage = "Y"
    if FindFlage == "Y" and SearchFlage == "N":
        OnlyFindFlage = "Y"

    if OnlyFindFlage == "Y" or "仅发现" in str(bookSourceName) or "仅发现" in str(bookSourceGroup):
        d["bookSourceGroup"] = d["bookSourceGroup"] + ";仅发现组"
    if bookSourceUrl is not None:
        d["bookSourceUrl"] = bookSourceUrl.strip()
        if SourceList.get(bookSourceUrl.strip()) is None:
            SourceList[bookSourceUrl.strip()] = d
        else:
            if SourceList[bookSourceUrl.strip()].get("lastUpdateTime", -1) < d.get("lastUpdateTime", -1):
                SourceList[bookSourceUrl.strip()] = d
        # print(bookSourceName, "---", d.get("bookSourceGroup"), "---", bookSourceUrl, "发现", FindFlage, "搜索", SearchFlage,
        #       "仅搜索", OnlyFindFlage)
    else:
        new_RSS_content.append(d)

SourceList = list(SourceList.values())
CheckList = []

pool_size = 64
pool = ThreadPool(pool_size)  # 创建一个线程池
pool.map(startcheck, SourceList)  # 往线程池中填线程
pool.close()  # 关闭线程池，不再接受线程
pool.join()

f = "yuedu_rss_source.json"
with open(f, "w") as file:
    file.write(json.dumps(new_RSS_content))
f = "yuedu_clear_source.json"
with open(f, "w") as file:
    # file.write(json.dumps(SourceList, sort_keys=True))
    file.write(json.dumps(sortSource(CheckList), sort_keys=True))
