from . import crawler
from flask import request, jsonify


@crawler.route('/test', methods=['POST'])
def add_character():
    # requestData = request.get_json(request.form)
    print(request.form['aaaa'])
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
    return jsonify(request.form)