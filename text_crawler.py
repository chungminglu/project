def crawler_pen(i):
    import requests
    import lxml
    from bs4 import BeautifulSoup as bs
    import re
    import time
    import pymongo
    from pymongo import MongoClient
    result = []
    i=i#頁數
    while True:
        print('開始載入網頁')
        # rec=re.compile('\。\[\]\/\/\.\(\)\s\+\～\、\，\-\❤\【\】\！\~\＆')
        res=requests.get('https://www.pixnet.net/searcharticle?q=%E4%BA%AC%E9%83%BD&type=related&period=year&page='+str(i))
        res.encoding='utf-8'## enconding 改為utf-8
        be=bs(res.text,'lxml')
        lists=be.select('ol.search-result > li.search-list')
        a_s=time.gmtime().tm_sec##開始秒數
        a_m=time.gmtime().tm_min##開始分鐘
        b=1#初始筆數
        for list1 in lists:
            info = {}
            Time=str(re.findall('([\d\-]+)\s',(list1.select('.search-postTime')[0]).text)).replace('\']','').replace('[\'','')
            info['時間']=Time
            human=str(re.findall('人氣\(\s([\d]+)\s',(list1.select('.search-views')[0]).text)).replace('\']','').replace('[\'','')
            info['人氣']=human
            info['來源']='痞客幫'
            for list2 in list1.select('a'):
                title=str(re.findall('title="([\w\。\[\]\/\/\.\(\)\s\+\～\、\，\-\❤\【\】\！\~\＆\／\（\）\《\》\@\&\;\‧]+)">',str(list2))).replace('\']','').replace('[\'','')
                if len(title)>5:
                    info['標題']=title
                author = str(re.findall('_blank">([\w]+)',str(list2))).replace('\']','').replace('[\'','')
                if (author == '繼續閱讀') | (author == '本篇之')|(author =='留言'):pass
                else:info['作者']=author
                url=str(re.findall('url=http%3A%2F%2F([\%\w\W]+)\" style',str(list2))).replace('%2F','/').replace('\']','').replace('[\'','')
                if len(url)>5:info['url']='http://'+url
            returns={}
            resq=requests.get(info['url'])
            resq.encoding='utf-8'
            be=bs(resq.text,'lxml')
            try:
                info['內文']=((be.select('div .article-content > div ')[0]).text).replace('\n','').replace('\xa0',' ').replace('\t','').replace(' ','')
            except:
                print('第{}頁第{}筆內文erro'.format(i,b))
                print('index out of range')
                info['內文']=''
                pass
            papers=be.select('div #comment-text')
            for paper in papers:
                views=paper.select('ul')
                for view in views:
                    try:
                        view1=((view.select('li')[2]).text).replace('\']','').replace('[\'','').replace('\n','').replace('\r','').replace(' ','')
                        returns['內容']=view1
                    except:
                        print('list index out of range')
                        pass
                    author=str(re.findall('title="([\w]+)"',str(view))).replace('\']','').replace('[\'','')
                    if len(author) < 1:
                        returns['作者']=''
                    elif len(author) > 1:
                        returns['作者']=author
                info['回文']=returns
                if len(info['回文']) < 1:
                    info['回文']=''
            print('現在筆數:{}'.format(b))
            b+=1##計算jason筆數
            result.append(info)
        print('第{}頁完成'.format(i))
        print(type(result))
        b_s=time.gmtime().tm_sec
        b_m=time.gmtime().tm_min
        spendTime=(b_m-a_m)*60+(b_s-a_s)
        if(b_m-a_m>0):
            print('花了{}秒'.format(spendTime))
        else:
            print('花了{}秒'.format(spendTime))
        if spendTime > 100 :
            print('連線逾時')
            print('目前頁數:{}'.format(i))
        if spendTime < 1 :
            raise Exception('秒數異常',spendTime)
        print('======')
#         print(result)
        if b > 10 :
            print('寫入Mongodb')
            client = MongoClient('10.120.27.11', 27017)
            db = client.test123
            collection = db['123456']
            collection.insert(result)
            print('第{}頁{}筆寫入成功'.format(i,b))
            result=[]#初始LIST
        i+=1###頁數

if __name__='__main__':
    import random
    proxy=['https://95.47.137.32:3128','https://139.59.125.77:8080','https://119.15.171.81:53281','https://46.101.96.46:80','https://192.118.76.136:80','https://139.59.125.12:80','https://128.199.75.123:80','https://49.213.16.207:80','https://128.199.190.243:3128','https://185.11.251.40:53281']
    #proxy[random.randrange(10)]##隨機亂數PROXY
    crawler_pen(i=1,proxy[random.randrange(10)])