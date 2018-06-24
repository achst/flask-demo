# -*- coding: utf-8 -*-
import logging
import sys
import gevent.monkey
from gevent.pywsgi import WSGIServer, WSGIHandler

from g import g
from util import logger, args, patch, wrapper
from util.router import Router
from router import router
from config import conf


def patch_flask(mode):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    gevent.monkey.patch_all(dns=False)
    patch.patch_conf(mode)


def init():
    g.conf = conf
    g.options, g.args = args.init()
    patch_flask(g.options.mode)

    g.logger = logger.init(g.options.port, g.conf)
    g.router = Router()
    g.app = g.router.app
    router.init(g.router)
    wrapper.init(g.app)


def main():
    listener = ('0.0.0.0', g.options.port)
    logging.info("Server running on %s:%s" % listener)
    http_server = WSGIServer(listener, g.app, handler_class=WSGIHandler)
    http_server.serve_forever()

if __name__ == '__main__':
    init()
    main()
