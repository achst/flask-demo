from handler import test


def init(r):
    r.get('/index', test.index)
    r.get('/test', test.test)
