import requests
from bs4 import BeautifulSoup as bs4
import pymongo
import datetime
import logging


class BaiduDistCrawler:
    def __init__(self, keyword):
        self.keyword = keyword
        self.mongo_client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.mongo_client.crawl
        self.baidu_dist_col = self.db['baidu_dist']

    def crawl(self):
        self.crawl_xiaobaipan(1)
        self.crawl_sowangpan(1)
        logging.info('百度网盘爬取完毕！')

    ''' 
    爬取每一页 
    Params: 从第几页开始
    '''
    def crawl_sowangpan(self, pageIndex):
        try:
            r = requests.get('http://www.sowangpan.com/search/' + self.keyword + '-0-全部-' + ('0' if pageIndex == 1 else str(pageIndex)) + '.html')
            r.encoding = 'utf-8'
            soup = bs4(r.text, 'lxml')
            list_all = soup.find_all(class_='main-x')
            if (len(list_all) > 0):
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
                                        logging.debug('url:' + 'http://www.sowangpan.com/search/' + self.keyword + '-0-全部-' + ('0' if pageIndex == 1 else str(pageIndex)) + '.html')
                                        logging.debug('link:' + key_btn.attrs['href'])
                                        insert_item = {
                                            'name': h3.find('a').text,
                                            'link': key_btn.attrs['href']
                                        }
                                        self.import_mongo(insert_item)
                        except Exception as e:
                            logging.error(e)
                self.crawl_sowangpan(pageIndex + 1)
        except requests.RequestException as e:
            logging.error(e)

    def crawl_xiaobaipan(self, pageIndex):
        try:
            r = requests.get('https://www.xiaobaipan.com/list-' + self.keyword + '-p' + str(pageIndex) + '.html')
            r.encoding = 'utf-8'
            soup = bs4(r.text, 'lxml')
            list_all = soup.find_all(class_='item-list job-item')
            if (len(list_all) > 0):
                for item in list_all:
                    job_title = item.find(class_='job-title')
                    if job_title:
                        title_a = job_title.find('a')
                        if title_a:
                            logging.debug('url:' + 'https://www.xiaobaipan.com/list-' + self.keyword + '-p' + str(pageIndex) + '.html')
                            logging.debug('link:' + 'https://www.xiaobaipan.com' + title_a.attrs['href'])
                            insert_item = {
                                'name': title_a.text,
                                'link': 'https://www.xiaobaipan.com' + title_a.attrs['href']
                            }
                            self.import_mongo(insert_item)
                self.crawl_xiaobaipan(pageIndex + 1)
        except requests.RequestException as e:
            logging.error(e)

    def import_mongo(self, item):
        try:
            item['create_time'] = datetime.datetime.now()
            # 添加前先删除
            self.baidu_dist_col.delete_one({'name': item['name'], 'link': item['link']})
            result = self.baidu_dist_col.insert(item)
        except Exception as e:
            logging.error(e)