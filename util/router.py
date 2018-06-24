from flask import Flask


class Router(object):

    def __init__(self):
        self.app = Flask(__name__, static_url_path='', static_folder='../static', template_folder='../template')

    def get(self, url, handler):
        self.app.add_url_rule(url, view_func=handler, methods=['GET'])

    def post(self, url, handler):
        self.app.add_url_rule(url, view_func=handler, methods=['POST'])
