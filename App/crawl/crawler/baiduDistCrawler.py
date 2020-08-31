import requests
from bs4 import BeautifulSoup as bs4
import pymongo
import datetime


class BaiduDistCrawler:
    def __init__(self, keyword):
        self.keyword = keyword
        self.mongo_client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.mongo_client.crawl

    def crawl(self):
        self.crawlSowangpan(1)

    ''' 
    爬取每一页 
    Params: 从第几页开始
    '''
    def crawlSowangpan(self, page):
        r = requests.get('http://www.sowangpan.com/search/' + self.keyword + '-0-全部-' + ('0' if page == 1 else str(page)) + '.html')
        r.encoding = 'utf-8'
        soup = bs4(r.text, 'lxml')
        list_all = soup.find_all(class_='main-x')
        if (len(list_all) > 0):
            baidu_dist_col = self.db['baidu_dist']
            for item in list_all:
                h3 = item.find(class_='x-left-h3')
                detail_href = h3.find('a').attrs['href']
                if detail_href:
                    try:
                        detail_r = requests.get(detail_href)
                        detail_r.encoding = 'utf-8'
                        detail_soup = bs4(detail_r.text, 'lxml')
                        key_btns = detail_soup.find_all(class_='main-xzfx-a')
                        if (key_btns and len(key_btns) > 0):
                            for key_btn in key_btns:
                                if (key_btn.text == '进入百度网盘下载'):
                                    print(h3.find('a').text)
                                    print(key_btn.attrs['href'])
                                    insert_item = {
                                        'name': h3.find('a').text,
                                        'link': key_btn.attrs['href'],
                                        'create_time': datetime.datetime.now()
                                    } 
                                    result = baidu_dist_col.insert(insert_item)
                    except Exception as e:
                        print(e)
            self.crawlSowangpan(page + 1)