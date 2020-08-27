import requests
from bs4 import BeautifulSoup as bs4


class BaiduDistCrawler:
    def __init__(self, keyword):
        self.keyword = keyword

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
            for item in list_all:
                h3 = item.find(class_='x-left-h3')
                print(h3.find('a').attrs['href'])
                print(h3.find('a').text)
            self.crawlSowangpan(page + 1)