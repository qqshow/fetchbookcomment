# -*- coding: utf-8 -*-
import re ,urllib
isbns = []

class GetDangdangDoubanAmazonUrl():
    def __init__(self, sUrl):
        self.startUrl = sUrl
        self.isbns = []
        #isbnRegex = regex1

    def controlSpider(self):
        isbn = self.getISBN(self.startUrl)
        
        if isbn:
            #解析当当网的url
            myID = self.getDangdangUrl(isbn) 
            if myID:
                ddUrl = 'http://comm.dangdang.com/reviewlist/' + myID +'/showall/?sort=useful&setcount=20'
            else:
                print 'can not parse the dangdang\'s ID at ISBN ' + isbn
                ddUrl =''


            #解析豆瓣网的url
            myID = self.getDoubanUrl(isbn) 
            if myID:
                doubanUrl = 'http://www.douban.com/subject/' + myID +'/reviews'
            else:
                print 'can not parse the douban\'s ID at ISBN ' + isbn
                doubanUrl = ''

            
            #解析亚马逊卓越的url
            amazonUrl = 'http://www.amazon.cn/mn/productReviewApplication?uid=168-6258410-2196214&prodid='\
                        + self.startUrl.replace('http://www.amazon.cn/dp/','')
            self.getBookInfo(isbn, self.startUrl)
            self.getAmazonCom(isbn, amazonUrl)
            self.getDangdangCom(isbn, ddUrl)
            self.getDoubanCom(isbn, doubanUrl)
            isbns.append(isbn)

    def getBookInfo(self, isbn, url):
        content = self.getContent(url)
        rNameImage = re.compile('id="ImageShow" alt="(.+?)" src="(.+?)" border=')
        rAuthor = re.compile('<title>.+?/(.+?)-')
        rPrice = re.compile('<span class="PriceCharacter">￥</span>(.+?)</strike>')
        rOther = re.compile('<span class="dark">(.+?)<br />')
        bookName = ''
        bookImage = ''
        author = ''
        price = ''
        other = ''
        m = rNameImage.findall(content)
        for n in m:
            bookName = n[0]
            bookImage = n[1]
        m = rAuthor.findall(content)
        for n in m:
            author = n
        m = rPrice.findall(content)
        for n in m:
            price = n
        m = rOther.findall(content)
        
        for n in m:
            if n.find('ISBN') == -1:
                other = other + n.replace('</span>', '') + '\n'
        fileName = isbn + '_info.txt'
        file = open(fileName,'w')
        file.write(bookName + '\n' + bookImage + '\n作者：' + author + '\n原价：' + price + '\n' + other)
        file.close()

        
    def errorSave(self, error):
        file = open('error.txt','a')
        file.write(error)
        file.close()

    def getAmazonCom(self,isbn,Url):
        content = self.getContent(Url)
        rTotal = re.compile('共有(\d+?)位顾客参与打分')
        m = rTotal.findall(content)
        if m:
            totalPage = (int(m[0]) / 10) + 1
            if totalPage > 10:
                totalPage = 10
        else:
            totalPage = 1
        fileName = isbn + '_Amazon.txt'
        #r = re.compile('<div id="\d+".*?>(.+?)<a href=', re.I|re.U|re.S)
        r = re.compile('<span class="tiny">([-: \d]+?)</span>.+?<div id="\d+".*?>(.+?)<a href=', re.I|re.U|re.S)
        moreCommPage = '<a target="_blank" href="http://click.linktech.cn/?m=joyo&a=A100013618&l=99999&l_cd1=0&l_cd2=1&tu=' \
                           + urllib.quote(Url) + '">亚马逊详细评论</a>'
        for i in range(1, totalPage+1):
            content = self.getContent(Url + '&page=' + str(i))
            m = r.findall(content)
            file = open(fileName,'a')
            
            for n in m:
                file.write('<span class="userN">亚马逊网友</span><br><br>' + n[1].strip() + \
                           moreCommPage + '<br><br>' + n[0] +'\n**********\n')
                moreCommPage = ''
                
            file.close()
            print Url + '&page=' + str(i) + 'save sucessfully.'


    def getDangdangCom(self,isbn,Url):
        content = self.getContent(Url)
        rTotal = re.compile('<em>(\d+?)</em>')
        m = rTotal.findall(content)
        if m:
            totalPage = (int(m[0]) / 20) + 1
            if totalPage > 5:
                totalPage = 5
        else:
            totalPage = 1
        fileName = isbn + '_Dangdang.txt'
        #r = re.compile("<div class='center_border'><div class='appear_time'>.+?</div><p>(.+?)</p></div>", re.I|re.U|re.S)
        r = re.compile("<div class='center_border'><div class='appear_time'>(.+?)</div><p>(.+?)</p></div>", re.I|re.U|re.S)
        moreCommPage = '<a target="_blank" href="http://click.linktech.cn/?m=dangdang&a=A100013618&l=99999&l_cd1=0&l_cd2=1&tu=' + \
                           urllib.quote(Url) + '">' + '当当网详细评论'.decode('utf-8').encode('gbk') + '</a>'
        for i in range(1, totalPage+1):
            content = self.getContent(Url + '&page=' + str(i))
            m = r.findall(content)
            file = open(fileName,'a')
            
            for n in m:
                file.write('<span class="userN">' + '当当网友'.decode('utf-8').encode('gbk') + '</span><br><br>' + \
                           n[1].strip() + moreCommPage + '<br><br>' + n[0] +'\n**********\n')
                moreCommPage = ''
            file.close()
            print Url + '&page=' + str(i) + 'save sucessfully.'
                
    def getDoubanCom(self,isbn,Url):
        content = self.getContent(Url)
        rTotal = re.compile('共(\d+?)条')
        m = rTotal.findall(content)
        if m:
            totalPage = (int(m[0]) / 25) + 1
            if totalPage > 4:
                totalPage = 4
        else:
            totalPage = 1
        fileName = isbn + '_Douban.txt'
        #r = re.compile("<div id='review_\d+?_short'>(.+?)<[aspan]+? class=", re.I|re.U|re.S)
        r = re.compile("<div id='review_\d+?_short'>(.+?)<[as].+? class=\"pl\">(.+?) ", re.I|re.U|re.S)
        moreCommPage = '<a target="_blank" href="' + Url + '">豆瓣网详细评论</a>'
        for i in range(1, totalPage+1):
            content = self.getContent(Url + '?start=' + str((i-1) * 25))
            m = r.findall(content)
            file = open(fileName,'a')
            
            for n in m:
                file.write('<span class="userN">豆瓣网友</span><br><br>' + n[0].strip() + \
                           moreCommPage + '<br><br>' + n[1] + '\n**********\n')
                moreCommPage = ''
                
            file.close()
            print Url + '?start=' + str((i-1) * 25) + 'save sucessfully.'

    

    def getDangdangUrl(self, isbn):
        content = self.getContent('http://search.dangdang.com/search.aspx?selectcatalog=&key=' + isbn + '&search=%CB%D1+%CB%F7&catalog=&SearchFromTop=1')
        r = re.compile("<h2><a href='http://search.dangdang.com/rd.asp.id=(\d+?)&")
        m = r.findall(content)
        for n in m:
            return n
        self.errorSave('can not parse Douban\'s Url at http://search.dangdang.com/search.aspx?selectcatalog=&key=' + isbn + '&search=%CB%D1+%CB%F7&catalog=&SearchFromTop=1 \n')
        return ''

    def getDoubanUrl(self, isbn):
        content = self.getContent('http://www.douban.com/subject_search?search_text=' + isbn )
        r = re.compile('<a href="/subject/(\d+?)/')
        m = r.findall(content)
        for n in m:
            return n
        self.errorSave('can not parse dangdang\'s Url at http://www.douban.com/subject_search?search_text=' + isbn + '\n')
        return ''
                
    def getISBN(self,url):
        content = self.getContent(url)
		#r = re.compile('条形码：</span>(\d+?)<br />')
        r = re.compile('条形码:</b>\s*(\d+)</li>')
        m = r.findall(content)
        for n in m:
            return n
        self.errorSave('can not get ISBN at ' + url + '\n')
        return ''
    
    

        
    def getContent(self,url):
        try:
            openurl = urllib.urlopen(url)
            content = openurl.read()
            openurl.close()
            return content
        except:
            print 'error in geting url' + url
            self.errorSave('error in geting url ' + url + '\n')
            return ''
    


if __name__=='__main__':
    file = open('detailurl.txt','r')
    urlList = file.read().split('\n')
    file.close()
    for i in urlList:
        #print i
        g = GetDangdangDoubanAmazonUrl(i)
        g.controlSpider()
    file = open('isbn.txt','w')
    file.write('\n'.join(isbns))
    file.close()