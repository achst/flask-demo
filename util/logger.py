import os
import logging
import logging.handlers

FORMAT = "%(asctime)s - %(levelname)s in %(funcName)s [%(pathname)s:%(lineno)d]\n%(message)s\n"


def log_config(key, filename, level='INFO', backup=7):
    log = logging.getLogger(key)
    log.setLevel(level.upper())
    log.handlers = []
    formatter = logging.Formatter(FORMAT)

    file_handler = logging.handlers.TimedRotatingFileHandler(filename=filename, when='midnight', backupCount=backup)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    return log


def init(port, conf):
    filename = os.path.join(os.path.dirname(__file__), "../log/{}.access.log".format(port))
    sys_log_filename = os.path.join(os.path.dirname(__file__), "../log/{}.all.log".format(port))
    log_config(None, sys_log_filename, conf.log_level, conf.log_file_backups_num)
    return log_config('default', filename, conf.log_level, conf.log_file_backups_num)
