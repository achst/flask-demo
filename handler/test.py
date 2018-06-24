from flask import render_template
from g import g
from g import errors
from base import common_dec, json_response


def index():
    return render_template('index.html')


@common_dec(login_required=True, validate_rule=['name'])
def test():
    # raise errors.BizError(u"hello")
    g.logger.info("test " * 100)
    return json_response(data={'hello': 'world'})
