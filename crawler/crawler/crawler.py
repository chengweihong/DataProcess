#!/usr/bin/python
#-*-utf-8-*-
"""
程序：多线程定向网页抓取与存储
coder：weihong.cwh
date：2011.11.22
"""
import sys
import urllib2
import urllib
import threading
import re
import Queue
from BeautifulSoup import *
from urlparse import *
import cPickle

#爬虫线程
class crawler(threading.Thread):
    def __init__(self,urlqueue,outqueue):
        threading.Thread.__init__(self)
        self.urlqueue = urlqueue
        self.outqueue = outqueue
        self.urlset = set()
        pass
    def __del__(self):
        pass
    def run(self):
        self.crawl(page)
    def dbcommit(self):
        pass
    def getentryid(self,table,field,value,createnew=True):
        return None
    def addtoindex(self,url,soup):
        #print 'indexing %s' %url
        pass
    def getText(self,soup,url):
        record = 'url: ' + url + '\n'
        title = soup('span')
        for item in title:
            if 'class' in dict(item.attrs):
                if 'question-title' in item['class']:
                    #print "title: ",item.contents[0]
                    #self.htmlfile.write("title: "+item.contents[0]+'\n')
                    record += 'title:  ' + item.contents[0] + '\n'
        bestlist = soup('pre')
        for item in bestlist:
            tag = item.findNext('pre',{'id':'best-answer-content'})
            if tag != Null:
                #print "tag: ",tag.contents[0]
                #self.htmlfile.write("tag: "+tag.contents[0]+'\n')
                #对不符合条件的的tag进行过滤，主要是带链接的
                try:
                    record += 'contents:  ' + tag.contents[0] + '\n'
                    self.outqueue.put(record)
                except Exception,e:
                    print e,tag,url
              
            #print "answer: ",item.findNext('pre',{'id':'best-answer-content'}).contents[0]
      
    def separatewords(self,text):
        return None
    def isindexed(self,url):
        m = re.findall("question/(\d+)\.html",url)
        if m == None or (m != None and m[0] in urlSet):
            return True
        else:    
            return False
    def addlinkref(self,urlFrom,urlTo,linkText):
        pass
    def crawl(self,pages,depth=2):
        print"crawl start!"
        crawlnum = 0
        while True:
            #print crawlnum
            crawlnum += 1
            page = self.urlqueue.get()
            #不能打开的链接过滤
            try:
                c = urllib2.urlopen(page)
            except:
                print "could not open %s" %page
                self.urlqueue.task_done()
                continue
            
            #c = urllib2.urlopen(page)
            urlcontent =  c.read()
            soup = BeautifulSoup(urlcontent)
            self.addtoindex(page,soup)
            links = soup('a')
            for link in links:
                if 'href' in dict(link.attrs):
                    if not 'question' in link['href']:
                        continue
                    url = urljoin(page,link['href'])
                    #print 'join url: ', url,"content: ",link.contents[0]
                    url = url.split('#')[0]
                    if url[0:4]=='http' and not self.isindexed(url) and crawlnum < 500:
                        #self.urlset.add(url)
                        m = re.findall("question/(\d+)\.html",url)
                        if m != None:
                            urlSet.add(m[0])
                        self.urlqueue.put(url)
            if 'question' in page:
                self.getText(soup,page)
                pass
            self.urlqueue.task_done()
            
#文本处理与存储线程
class TextProcessandSave(threading.Thread):
    def __init__(self,outqueue,filename):
        threading.Thread.__init__(self)
        self.outqueue = outqueue
        self.datafile = file(filename,"w")
    def __del__(self):
        self.datafile.close()
    def run(self):
        print 'text process start'
        self.savefilenum = 0
        while True:
            self.savefilenum += 1
            if self.savefilenum%1000 == 0:
                print "save file: ",self.savefilenum
                cPickle.dump(urlSet,urlSetFile)
                print "save url set: "
            pagetext = self.outqueue.get()
            #print "get content:  ",pagetext
            filttext = self.processText(pagetext)
            self.saveText(filttext)
            self.outqueue.task_done()
    def processText(self,text):
        return text
    def saveText(self,text):
        #无法正确解码存储的文件过滤掉
        try:
            self.datafile.write(text)
        except Exception,e:
            print e,text

#...........................MAIN......................................../
urlqueue = Queue.Queue()
outqueue = Queue.Queue()
urlSetFile = file("./page/urlsetfile","wr")
urlSet = cPickle.load(urlSetFile)
page = ["http://zhidao.baidu.com/browse/160?lm=0&word=&pn=0"]
def main():
    print "main start"
    print sys.getdefaultencoding()
    for i in range(0,50):
        spider = crawler(urlqueue,outqueue)
        spider.setDaemon(True)
    #spider.crawl(page)
        spider.start()
    urlqueue.put(page[0])
    backend = TextProcessandSave(outqueue,"./page/2011.12.3")
    backend.setDaemon(True)
    backend.start()
    urlqueue.join()
    outqueue.join()
    urlSetFile.close()
    print 'carwler over!'
if __name__=='__main__':
    main()
                    
    
