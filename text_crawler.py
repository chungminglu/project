import requests
import lxml
from bs4 import BeautifulSoup as bs
import re
result = []
info = {}
i=1
while True:
    res=requests.get('https://www.pixnet.net/searcharticle?q=%E4%BA%AC%E9%83%BD&type=related&period=year&page='+str(i))
    res.encoding='utf-8'## enconding 改為utf-8
    be=bs(res.text,'lxml')
    lists = be.select('ol.search-result > li.search-list')
    for list1 in lists:
        time = str(re.findall('([\d\-]+)\s', (list1.select('.search-postTime')[0]).text)).replace('\']', '').replace(
            '[\'', '')
        info['時間'] = time
        human = str(re.findall('人氣\(\s([\d]+)\s', (list1.select('.search-views')[0]).text)).replace('\']', '').replace(
            '[\'', '')
        info['人氣'] = int(human)
        info['來源'] = '痞客幫'
        for list2 in list1.select('a'):
            title = str(re.findall('title="([\w\。\[\]\/\/\.\(\)\s\+\～\、\，\-\❤\【\】\！\~\＆\／\（\）\《\》\@\&\;\‧]+)">',
                                   str(list2))).replace('\']', '').replace('[\'', '')
            if len(title) > 5:
                info['標題'] = title
            author = str(re.findall('_blank">([\w]+)', str(list2))).replace('\']', '').replace('[\'', '')
            if (author == '繼續閱讀') | (author == '本篇之') | (author == '留言'):
                pass
            else:
                info['作者'] = author
            url = str(re.findall('url=http%3A%2F%2F([\%\w\W]+)\" style', str(list2))).replace('%2F', '/').replace('\']',
                                                                                                                  '').replace(
                '[\'', '')
            if len(url) > 5:
                info['url'] = 'http://' + url
    returns = {}
    resq = requests.get(info['url'])
    resq.encoding = 'utf-8'
    be = bs(resq.text, 'lxml')
    info['內文']=((be.select('div .article-content > div ')[0]).text).replace('\n','').replace('\xa0',' ').replace('\t','').replace(' ','')
    papers=be.select('div #comment-text')
    for paper in papers:
        views = paper.select('ul')
        for view in views:
            try:
                view1=((view.select('li')[2]).text).replace('\']','').replace('[\'','').replace('\n','').replace('\r','').replace(' ','')
                returns['內容']=view1
            except:
                print('list index out of range')
                pass
            author = str(re.findall('title="([\w]+)"', str(view))).replace('\']', '').replace('[\'', '')
            if len(author) > 1:
                returns['作者']=author
    info['回文']=returns
    print('======')
    print(info)