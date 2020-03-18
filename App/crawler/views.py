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


@crawler.route('/testCrawler', methods=['POST'])
def testCrawler():
    r = requests.get('https://www.720mp4.com/')
    r.encoding = 'gb2312'
    soup = bs4(r.text, 'lxml')
    title_all = soup.find_all(class_="title_all")
    today_item = ''
    for item in title_all:
        if (item.find('span').text == '今日更新'):
            today_item = item
    print(today_item.next_sibling)
    res = '123'
    return res