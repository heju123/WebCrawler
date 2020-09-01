import os
from flask import Flask
from App.main import main as main_blueprint
from App.crawl import crawl as crawl_blueprint
import logging
route_prefix = '/'


def create_app():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    APP_BASE_DIR = os.path.join(BASE_DIR, 'app')
    templates_dir = os.path.join(APP_BASE_DIR, 'templates')
    static_dir = os.path.join(APP_BASE_DIR, 'static')
    app = Flask(__name__, static_folder=static_dir,
                template_folder=templates_dir)
    app.config["APPLICATION_ROOT"] = route_prefix
    app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=route_prefix)
    app.debug = True
    app.register_blueprint(blueprint=main_blueprint)
    app.register_blueprint(blueprint=crawl_blueprint)

    logging.basicConfig(level=logging.DEBUG)  # 设置日志级别
    return app


class PrefixMiddleware(object):
    """
    虚拟二级目录支持
    """

    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]