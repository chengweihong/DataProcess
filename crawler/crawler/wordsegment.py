#!/usr/bin/python
# -*- coding: utf-8 -*-
#对问题进行分词，统计词频
import sys
import os
import cPickle
from pymmseg import mmseg
mmseg.dict_load_defaults()
wordcountdict = dict()
text = file("./page/2011.12.3")#网页
wordcount = file("./Tmp/wordcount","w")#TF
count = 0
for line in text:
    #print line
    algor = mmseg.Algorithm(line)
    count+=1
    print count
    for tok in algor:
        #print '%s [%d..%d]' % (tok.text, tok.start, tok.end)
        wordcountdict[tok.text] = wordcountdict.get(tok.text,0) + 1

sortwordcount = sorted(wordcountdict.items(),key=lambda d:d[1],reverse=True)
cPickle.dump(sortwordcount, wordcount)
wordcount.close()
text = file("./Tmp/wordcounttext","w")
for word,count in sortwordcount:
    text.write(word+"\t"+str(count)+"\n")
print "over"
    
