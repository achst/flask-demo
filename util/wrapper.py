# -*- coding: utf-8 -*-
import logging
import datetime
import json
from flask import request
from g import g


def wrap_access_log(app):

    def write_access_log(response):
        if '200' not in response.status:
            return
        try:
            method = request.method.lower()
            # 返回数据
            res_data = json.loads(response.data) if response.data else {}

            # 请求数据
            if method == 'post' and 'application/json' in request.mimetype:
                req_data = request.get_json() if request.data else {}
            else:
                req_data = dict((key, request.values.get(key)) for key in request.values.keys())

            # 操作人信息
            opt_member = {k: g.login_member.get(k) for k in ('id', 'phone')} if hasattr(g, 'login_member') else {}

            log = {
                'method': method,
                'ip': request.remote_addr,
                'member': opt_member,
                'req_data': req_data,
                'res_data': res_data,
                'path': request.path,
                'datetime': '{}'.format(datetime.datetime.now())
            }
            log_string = json.dumps(log, encoding='utf-8', ensure_ascii=False)
            g.logger.info(log_string)
        except Exception as e:
            logging.warn(e)
            pass

    @app.after_request
    def _after_request(response):
        write_access_log(response)
        return response


def init(app):
    wrap_access_log(app)
