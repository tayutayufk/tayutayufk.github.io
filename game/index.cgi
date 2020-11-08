import cgitb
cgitb.enable()

from wsgiref.handlers import CGIHandler
from app import app
#-------------------以下、書き換え部分------------------------
from sys import path

path.insert(0, '/ropeproject/www/game/')
from app import app
class ProxyFix(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, environ, start_response):
        environ['SERVER_NAME'] = "ropeproject.sakura.ne.jp/"
        environ['SERVER_PORT'] = "80"
        environ['REQUEST_METHOD'] = "GET"
        environ['SCRIPT_NAME'] = ""
        environ['PATH_INFO'] = "/"
        environ['QUERY_STRING'] = ""
        environ['SERVER_PROTOCOL'] = "HTTP/1.1"
        return self.app(environ, start_response)
if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    CGIHandler().run(app)