#!/usr/bin/python
# -*- coding: utf-8 -*-
#计算关键词权重（tf）
import sys
import os
import cPickle



#keywordfile = file("keywords.txt")
#outputfile = file("keyword.txt","w")
#
#for line in keywordfile:
#    keyword = line[0:-1].split(" ")
#    for item in keyword:
#        try:
#            outputfile.write(str(len(item.decode("utf-8")))+" "+item+"\n")
#        except Exception,e:
#            print e,item
keywordTf = file("./worddict/keywordTf.txt","w")#权重文本形式
keywordWT = file("./worddict/keywordWT.txt","w")#权重结构化存储
keywordfile = file("./worddict/keyword.txt") 
wordcount = file("./Tmp/wordcounttext")  
stopword = file("./worddict/stopWord.txt") 
worddict = file("./worddict/word.dict")
#newworddict = file("./sitproject/word.dict","w")

wordcountdict = dict()
keywordsTf = dict()
keywordset = set()
stopwordset = set()
worddictset = set()

for line in worddict:
    len,word = line[0:-1].split(" ")
    worddictset.add(word)

for line in stopword:
    stopwordset.add(line[0:-1])

for line in keywordfile:
    len,keyword = line[0:-1].split(" ")
    keywordset.add(keyword)

for line in wordcount:
    word,count = line[0:-1].split("\t")
    wordcountdict[word] = count
countnum = 0

for item in keywordset:
    if item in wordcountdict:
        if int(wordcountdict[item]) >= 10:#如果关键词tf大于10则保留原tf否则设为10
            keywordTf.write(item+'\t'+wordcountdict[item]+"\n")
            keywordsTf[item] = int(wordcountdict[item])
        else:
            keywordTf.write(item+'\t'+"10"+"\n")
            keywordsTf[item] = 10
    else:#如果不在wordcount中，则设为5
        keywordTf.write(item+'\t'+"5"+"\n")
        keywordsTf[item] = 5
print countnum
cPickle.dump(keywordsTf, keywordWT)
countnum = 0
countn = 0
for item,count in wordcountdict.items():
    if item in keywordset:
        countnum+=1
    if item in stopwordset:
        countn+=1
print countnum
print countn

countnum = 0

for item,count in wordcountdict.items():
    if not item in worddictset:
        countnum+=1
        #print item
    else:
        pass
        #print item
print countnum
#    if word in keywordset:
#        continue
#    else:
#        newworddict.write(line)
#keywordfile.seek(0)
#for line in keywordfile:
#    newworddict.write(line)
#newworddict.close()
