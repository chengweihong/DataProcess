#!/usr/bin/python
# -*- coding: utf-8 -*-
#网页存储结构page,key:problemId  valuekey: url,title,content
#筛选问题
import sys
import os
import re
import cPickle
#from pymmseg import mmseg
#mmseg.dict_load_defaults()


pagefile = file("./page/pages","r")
pagedict = cPickle.load(pagefile)

print "load success!"
count = 0
for id,question in pagedict.items():
    if "吃什么" in question["title"] and "宝宝" in question["title"]:
        print id,question["title"]
        record = ""
        for word in question["titlevec"]:
            record += word + "  "
        print record
        count += 1
print count

#textfile = file("./page/2011.12.3")
#pagefile = file("./page/pages","w")
#
#pagedict = {}
#questionid = 0
#content = ""
#for line in textfile:
#    if "url:" in line:
#        if questionid in pagedict:
#            pagedict[questionid]["content"] = content
#            pagedict[questionid]["contentvec"] = []
#            algor = mmseg.Algorithm(content)
#            for tok in algor:
#                pagedict[questionid]["contentvec"].append(tok.text)
#            content = ""
#        m = re.findall("question/(\d+)\.html",line)
#        if m == None:
#            continue
#        questionid = m[0]
#        url = line[4:-1]
#        pagedict[questionid] = {"url":url}
#        print url
#    elif "title:" in line:
#        title = line[6:-1]
#        print title
#        pagedict[questionid]["title"] = title
#        pagedict[questionid]["titlevec"] = []
#        algor = mmseg.Algorithm(title)
#        for tok in algor:
#            pagedict[questionid]["titlevec"].append(tok.text)
#    elif "content:" in line:
#        content = line[7:-1]
#    elif line == "\n":
#        continue
#    else:
#        content += line
#        
#cPickle.dump(pagedict, pagefile)
#pagefile.close()
#print "over"