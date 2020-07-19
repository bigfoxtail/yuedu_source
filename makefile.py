#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import demjson
import requests

source_list = [
    "https://xiu2.github.io/yuedu/shuyuan",
    "http://alanskycn.gitee.io/vip/assets/import/book_source.json",
    "https://gitee.com/zmn1307617161/booksource/raw/master/%E4%B9%A6%E6%BA%90/%E7%B2%BE%E6%8E%923.txt",
    "https://gitee.com/haobai1/bookyuan/raw/master/shuyuan.json",
    "https://gitee.com/slght/yuedu_booksource/raw/master/%E4%B9%A6%E6%BA%90/API%E4%B9%A6%E6%BA%90_3.0.json",
]

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

source_content = []
for url in source_list:
    try:
        rs = requests.session()
        res = rs.get(url, headers=headers)
        res.encoding = 'utf-8'
        resjson = demjson.decode(res.text)
        source_content.extend(resjson)
    except Exception as e:
        pass

f = "yuedu_source.json"
with open(f, "w") as file:  # ”w"代表着每次运行都覆盖内容
    file.write(json.dumps(source_content))
