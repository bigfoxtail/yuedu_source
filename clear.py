#!/usr/bin/python
# -*- coding:utf-8 -*-
import json

source_content = []
new_source_content = []
new_RSS_content = []
SourceList = {}

with open("yuedu_source.json", 'r', encoding='utf-8') as file_to_read:
    resjson = json.loads(file_to_read.read())
    source_content.extend(resjson)

for d in source_content:
    bookSourceName = d.get("bookSourceName")
    bookSourceGroup = d.get("bookSourceGroup")
    bookSourceUrl = d.get("bookSourceUrl")

    FindFlage = "N"
    SearchFlage = "N"
    aa = d.get("searchUrl")
    if d.get("ruleFindUrl") is not None:
        FindFlage = "Y"
    if d.get("ruleSearchUrl") is not None or d.get("searchUrl") is not None:
        SearchFlage = "Y"
    OnlyFindFlage = "N"
    if FindFlage == "Y" and SearchFlage == "N":
        OnlyFindFlage = "Y"

    if OnlyFindFlage == "Y" or "仅发现" in str(bookSourceName) or "仅发现" in str(bookSourceGroup):
        d["bookSourceGroup"] = d["bookSourceGroup"] + ";仅发现组"
    if bookSourceUrl is not None:
        d["bookSourceUrl"] = bookSourceUrl.strip()
        new_source_content.append(d)
        if SourceList.get(bookSourceUrl.strip()) is None:
            SourceList[bookSourceUrl.strip()] = d
        else:
            if SourceList[bookSourceUrl.strip()].get("lastUpdateTime", -1) < d.get("lastUpdateTime", -1):
                SourceList[bookSourceUrl.strip()] = d
    else:
        new_RSS_content.append(d)
    # print(bookSourceName, bookSourceGroup, bookSourceUrl, "发现", FindFlage, "搜索", SearchFlage, "仅搜索", OnlyFindFlage)

SourceList = list(SourceList.values())

f = "new_yuedu_source.json"
with open(f, "w") as file:
    file.write(json.dumps(new_source_content))
f = "new_RSS_source.json"
with open(f, "w") as file:
    file.write(json.dumps(new_RSS_content))
f = "clear_yuedu_source.json"
with open(f, "w") as file:
    file.write(json.dumps(SourceList, sort_keys=True))
