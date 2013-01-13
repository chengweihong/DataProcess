#!/usr/bin/python
# -*- coding: utf-8 -*-
#kmeans计算问题聚类
import sys
import os
import cPickle
import random
import math
#编辑距离
class arithmetic():    
    def __init__(self):
        pass  
    def levenshtein(self,first,second):
        if len(first) > len(second):
            first,second = second,first
        if len(first) == 0:   
            return len(second)   
        if len(second) == 0:   
            return len(first)   
        first_length = len(first) + 1  
        second_length = len(second) + 1  
        distance_matrix = [range(second_length) for x in range(first_length)]    
        #print distance_matrix   
        for i in range(1,first_length):   
            for j in range(1,second_length):   
                deletion = distance_matrix[i-1][j] + 1  
                insertion = distance_matrix[i][j-1] + 1  
                substitution = distance_matrix[i-1][j-1]   
                if first[i-1] != second[j-1]:   
                    substitution += 1  
                distance_matrix[i][j] = min(insertion,deletion,substitution)   
        #print distance_matrix   
        return distance_matrix[first_length-1][second_length-1]   
#计算两个向量的欧式距离
def computedist(vec1,vec2,threshold):
    vectmp1 = vec1[:]
    vectmp2 = vec2[:]  
    sumdistanc = 0.0
    samerecord = ""
    vecdistanc = 0.0
    for word in vec1:
        if  word in vec2 and  word in vectmp1 and  word in vectmp2:
            vectmp1.remove(word)
            vectmp2.remove(word)
            vecdistanc+= keywordTf.get(word,1)*keywordTf.get(word,1)
            samerecord+=" "+word
    for word in vectmp1:
        sumdistanc += keywordTf.get(word,1)*keywordTf.get(word,1)
    tmp = sumdistanc
    for word in vectmp2:
        sumdistanc += keywordTf.get(word,1)*keywordTf.get(word,1)
    if sumdistanc<threshold:
        print "vec1:",tmp,"vec2:",sumdistanc-tmp,"sum:",sumdistanc,"same:",samerecord
    return vecdistanc,samerecord

#计算两个向量余弦相似度
def computecos(vec1,vec2):
    similarty = 0.0
    vec1mod = 0
    vec2mod = 0
    dotres = 0
    samerecord=""
    for word in vec1:
        vec1mod += keywordTf.get(word,1)*keywordTf.get(word,1)
        if word in vec2:
            dotres +=  keywordTf.get(word,1)*keywordTf.get(word,1)
            samerecord += " " + word + ": " + str(keywordTf.get(word,1))
    for word in vec2:
        vec2mod += keywordTf.get(word,1)*keywordTf.get(word,1)
    #print dotres,vec1mod,vec2mod
    if vec1mod * vec2mod != 0:
        similarty = dotres*1.0/(math.sqrt(vec1mod)*math.sqrt(vec2mod))
    return similarty,samerecord+" vec1mod: " + str(vec1mod) + " vec2mod: " + str(vec2mod)
    
#keywordTf = {"婴儿":1,"一般":2,"怎么办":1}
#v1=["婴儿","b","c"]
#v2=["婴儿","d"]
#dist=computedist(v1,v2)
#dist1=computecos(v1,v2)
#print dist,dist1
#sys.exit(0)
#.............................MAIN......................

ProCatNum = 100#200  #问题类别数
ProNum = 1000#24028   #总问题数
print "start"
pagefile = file("./page/pages","r")#网页存储
pagedict = cPickle.load(pagefile)
print "load page data success!"
keywordWT = file("./worddict/keywordWT.txt","r")#权重结构化存储
keywordTf = cPickle.load(keywordWT)
print "load keywordwt success!"
#testpagefile = file("./page/testpage2","w")
#testpagedict = dict()
num = 0
#随机生成种子
Proset = set()
seedcount = 0
while True:
    seed = random.randint(1,ProNum)
    if seed in Proset:
        continue
    Proset.add(seed)
    seedcount+=1
    if seedcount > ProCatNum:
        break
#根据随机生成的种子初始化聚类存储结构
print "seed generate success!"
ProCatDict = dict()#聚类存储结构
count = 0
for id,item in pagedict.items():
    count+=1
    num+=1

    if count in Proset:
        ProCatDict[id] = dict()
        ProCatDict[id]["label"] = count
        ProCatDict[id]["meanvec"] = pagedict[id]["titlevec"]
        ProCatDict[id]["seed"] = [id]
        print pagedict[id]["title"]
print "seed initalize!"

#迭代kmeans，求取全局最小类内距离
arith = arithmetic()   
#print arith.levenshtein( u'2岁孩子感冒怎么办',u''  )
SumDistance = 1000000000
SumRatio = 0.1
while True:
    for id,page in pagedict.items():
        mindistance = 1000
        minlable = 0
        minrecord = ""
        minpage = ""
        for id1,page1 in  pagedict.items():
            if id1!= id:
                #distance,samerecord = computedist(page["titlevec"],page1["titlevec"],0)
                distance,samerecord = computecos(page["titlevec"],page1["titlevec"])
                #distance = arith.levenshtein(page["titlevec"],page1["titlevec"])
                samerecord = ""
                if distance < mindistance:
                    mindistance = distance
                    minpage = page1["title"]
                    minrecord = samerecord
        print mindistance,"page1:",page["title"],"page2:",minpage,"same:",minrecord
        pass
#        for seed,cat in ProCatDict.items():
#            distance = computedist(page["titlevec"],cat["meanvec"],100000)
#            centre = ""
#            for w in cat["meanvec"]:
#                centre+=w
#            if distance < mindistance:
#                mindistance = distance
#                if distance < 100000:
#                    print page["title"],"    seed   ",centre
kmeansres = file("kmeansres","w")
cPickle.dump(ProCatDict, kmeansres, True)
print "end"


