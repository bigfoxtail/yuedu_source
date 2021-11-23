#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
# import demjson 效率极低，早期为了应对非标json使用
import requests


def delete_duplicate_str(data):
    immutable_dict = set([str(item) for item in data])
    data = [eval(i) for i in immutable_dict]
    return data


source_list = [
    # RSS 官方源 不好用 混起来会有问题 https://gitee.com/alanskycn/yuedu/raw/master/JS/RSS/custom/customRss.json",

    # RSS
    "https://shuyuan.miaogongzi.net/shuyuan/1633030418.json",

    "https://github.com/xdd666t/MyData/raw/master/novel/bookshelf/14个发现书源.txt",
    "https://github.com/xdd666t/MyData/raw/master/novel/bookshelf/54个优质书源(14个发现).xml",
    "https://github.com/xdd666t/MyData/raw/master/novel/bookshelf/768个校对书源.txt",
    "https://github.com/xdd666t/MyData/raw/master/novel/bookshelf/868个分组书源(逐个校对的).txt",
    "https://github.com/xdd666t/MyData/raw/master/novel/bookshelf/N个书源(长期更新).txt",
    "https://github.com/xdd666t/MyData/raw/master/novel/bookshelf/N个优质书源.txt",

    "https://github.com/xdd666t/MyData/raw/master/novel/read3.0/N_booksource.json",
    "https://github.com/xdd666t/MyData/raw/master/novel/read3.0/nice_booksource.json",

    "https://github.com/xdd666t/MyData/raw/master/novel/155个自留优质书源（不含H）.txt",
    "https://github.com/xdd666t/MyData/raw/master/novel/1700个自用书源.json",
    "https://github.com/xdd666t/MyData/raw/master/novel/484个优质书源.txt",
    "https://github.com/xdd666t/MyData/raw/master/novel/66个精品书源.json",

    "https://gitlab.com/GJTQQ/YueDu/raw/master/Share/915.json",
    "https://gitlab.com/GJTQQ/YueDu/raw/master/Share/425.json",
    "https://gitlab.com/GJTQQ/YueDu/raw/master/Share/WxSource.json",
    "https://gitlab.com/GJTQQ/YueDu/raw/master/Share/雨则10.16二次校验_854个书源_.json",

    "https://www.lifves.com/api/v2/booksource/list",

    "https://gedoor.github.io/MyBookshelf/bookSource.json",
    "http://www.legado.top/MyBookshelf/bookSource.json",

    "https://yuedu.xiu2.xyz/shuyuan",

    "http://no-mystery.gitee.io/shuyuan/全网通用.json",

    "https://raw.githubusercontent.com/XIU2/Yuedu/master/shuyuan",

    "http://alanskycn.gitee.io/vip/assets/import/book_source.json",
    "http://alanskycn.gitee.io/vip/assets/import/bs.json",
    "https://gitee.com/slght/yuedu_booksource/raw/master/书源/API书源_3.0.json",

    # 失效 "https://celeter.github.io/SourceGo/book_source/all.json",

    "http://alanskycn.gitee.io/vip/assets/import/audio_source.json",

    "https://cdn.jsdelivr.net/gh/yeyulingfeng01/yuedu.github.io@1.1/202003.txt",
    "https://cdn.jsdelivr.net/gh/yeyulingfeng01/yuedu.github.io/yeudu3.0-202005.json",

    "https://moonbegonia.github.io/Source/yuedu/audio.json",

    "https://moonbegonia.github.io/Source/yuedu/fullSourceIncludeInvalid.json",

    # 失效 "https://xiu2.github.io/yuedu/shuyuan",

    # 失效 "https://gitee.com/zmn1307617161/booksource/raw/master/书源/精排3.txt",
    "https://guaner001125.coding.net/p/coding-code-guide/d/booksources/git/raw/master/sources/guaner.json",
    "https://gitee.com/haobai1/bookyuan/raw/master/shuyuan.json",

    "http://shuyuan.miaogongzi.site/shuyuan/1614645247.json",
    "http://shuyuan.miaogongzi.site/shuyuan/1614644339.json",

    "https://shuyuan.miaogongzi.net/shuyuan/1633024206.json",
    "http://www.yckceo.com/d/y1CBQ",
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

# 手动写死算了 省事 谁知道以后要不要单独处理
with open("./book/BookSource.json", 'r', encoding='utf-8') as file_to_read:
    resjson = json.loads(file_to_read.read().replace('\n', ""))
    source_content.extend(resjson)
with open("./book/OldBookSource.json", 'r', encoding='utf-8') as file_to_read:
    resjson = json.loads(file_to_read.read().replace('\n', ""))
    source_content.extend(resjson)
with open("./book/RSSSource.json", 'r', encoding='utf-8') as file_to_read:
    resjson = json.loads(file_to_read.read().replace('\n', ""))
    source_content.extend(resjson)

for url in source_list:
    try:
        rs = requests.session()
        res = rs.get(url, headers=headers)
        res.encoding = 'utf-8'
        resjson = json.loads(res.text.replace('\n', ""))
        source_content.extend(resjson)
        print("下载成功", url)
    except Exception as e:
        print("下载错误", url)
        print('repr(e):\t', repr(e))
        pass

f = "yuedu_source.json"
with open(f, "w") as file:
    content = json.dumps(source_content, sort_keys=True)
    content = json.loads(content)
    content = delete_duplicate_str(content)
    file.write(json.dumps(content, sort_keys=True))
