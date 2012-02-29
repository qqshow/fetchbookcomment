# -*- coding: utf-8 -*-
import urllib,re,time

class spider:
    def __init__(self, sUrl,detailRegex, listRegex):
        self.listUrls=[sUrl]
        self.detailUrls=[]
        self.detailRegex = detailRegex
        self.listRegex = listRegex
        

    def controlSpider(self):
        cnt = 0
        for i in self.listUrls:
            self.getDetailUrl(i)
            self.getListUrl(i)
            cnt = cnt + 1
            print 'begin to crawl' + i
            print cnt
            time.sleep(2)
        self.saveDetailUrl() #保存详细页面的url
            
    def getDetailUrl(self,url):
        content = self.getContent(url)
        r = re.compile(self.detailRegex, re.I|re.U|re.S)
        m = r.findall(content)
        for n in m:
            if n not in self.detailUrls:
                self.detailUrls.append(n)
                print 'find ' + n + ', and add it to detail list.'

    
    def getListUrl(self, url):
        content = self.getContent(url)
        r = re.compile(self.listRegex, re.I|re.U)
        m = r.findall(content)
        for n in m:
            if n not in self.listUrls:
                self.listUrls.append(n)
                print 'find ' + n + ', and add it to list page.'

    def getContent(self,url):
        try:
            openurl = urllib.urlopen(url)
            content = openurl.read()
            openurl.close()
            return content
        except:
            print 'error in geting url' + url
            return ''

    def saveDetailUrl(self):
        file = open('detailurl.txt','w')
        file.write('\n'.join(self.detailUrls))
        file.close()


if __name__=='__main__':
    startUrl='http://www.amazon.cn/mn/rank?nodeid=51080&page=1&uid=168-6258410-2196214'
    detailRegex = '<div class="pic"><a href="(http://www.amazon.cn/dp/[0-9a-z]+)"><img'
    #listRegex = '<a href="(http://www.amazon.cn/mn/[store]*?rank.+?)"'
    listRegex = '<a href="(http://www.amazon.cn/mn/rank.nodeid=51080.+?)"'
    s = spider(startUrl, detailRegex, listRegex)
    s.controlSpider() #把detail页面打印出来，并保存为txt文件。
    print 'Finish crawling。。。。。。'
