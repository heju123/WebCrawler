from . import crawler
from flask import request, jsonify
import requests
from bs4 import BeautifulSoup as bs4


@crawler.route('/test', methods=['POST'])
def test():
    # requestData = request.get_json(request.form)
    ret = request.form.to_dict()
    print(ret['aaaa'])
    print(request.form)
    responseData = [
            {
                "id": 1,
                "name": "张三",
                "group": "/XX省/xx市/xx领导/",
                "newgroup": "/xxx省/xxx市/xx县/",
                "newname": "李四",
                "newNote": ""
            }
        ]
    ret['test'] = '12313'
    return jsonify(ret)


@crawler.route('/crawlerBaiduDist', methods=['POST'])
def crawlerByKeyword():
    keyword = request.form.get('keyword')
    r = requests.get('http://www.sowangpan.com/search/' + keyword + '-0-全部-0.html')
    r.encoding = 'utf-8'
    soup = bs4(r.text, 'lxml')
    list_all = soup.find_all(class_='main-x')
    for item in list_all:
        h3 = item.find(class_='x-left-h3')
        print(h3.find('a').attrs['href'])
        print(h3.find('a').text)
    return 'success'