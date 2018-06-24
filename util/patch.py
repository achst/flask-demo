import inspect
from config import conf
from config import devconf


def patch_conf(mode='dev'):
    modes = {'dev': devconf, 'deploy': conf}
    if mode not in modes:
        raise Exception("can't support this mode")
    for k, _ in inspect.getmembers(conf):
        if not k.startswith('__'):
            v = getattr(modes[mode], k)
            setattr(conf, k, v)
