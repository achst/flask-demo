# -*- coding: utf-8 -*-


class BizError(Exception):

    def __init__(self, message=None, data=None, code=-1):
        self.code = code
        self.data = data
        self.message = message

    def __str__(self):
        message = self.message
        if isinstance(message, unicode):
            message = message.encode('utf-8')

        return '<%d %s>' % (self.code, message)

ErrNormal = BizError(code=100, message=u'自定义错误')
ErrNotLogin = BizError(code=200, message=u'用户未登陆')
ErrArgs = BizError(code=300, message=u'请求参数/格式错误')
ErrNotFound = BizError(code=400, message=u'资源不存在')
ErrServerInternal = BizError(code=500, message=u'服务器异常')
