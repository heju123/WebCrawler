from . import main
from flask import render_template, make_response


@main.after_request
def af_request(resp):
    """
    # 请求钩子，在所有的请求发生后执行，加入headers。
    :param resp:
    :return:
    """
    resp = make_response(resp)
    resp.headers["Server"] = "Heju personal server"
    return resp


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')