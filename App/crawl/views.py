from . import crawl
from flask import request, jsonify
from App.crawl.crawler.baiduDistCrawler import BaiduDistCrawler
import threading


@crawl.route('/crawl/test', methods=['POST'])
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


@crawl.route('/crawl/crawlBaiduDist', methods=['POST'])
def crawlerByKeyword():
    keyword = request.form.get('keyword')
    baiduDistCrawler = BaiduDistCrawler(keyword)
    thread = threading.Thread(target=baiduDistCrawler.crawl)
    thread.start()
    return 'success'