# -*- coding: utf-8 -*-
import functools
from flask import jsonify, g, request
from util import common
from g.errors import BizError, ErrArgs


def get_page_params():
    args = request.args
    page = args.get('page', type=int, default=1)
    if page == 0:
        page = 1
    page_size = args.get('page_size', type=int, default=10)
    return page, page_size


def json_response(code=0, data=None, message=None):
    rst_dict = dict(code=code)
    if message:
        rst_dict['message'] = message
    if data:
        data_dict = common.serializer(data)
        rst_dict['data'] = data_dict
    else:
        rst_dict['data'] = None if data is None else data
    return jsonify(rst_dict)


def common_dec(login_required=None, validate_rule=None):
    def handle_func(func):
        @functools.wraps(func)
        def do_check(*args, **kwargs):
            try:
                # 登陆校验
                if login_required:
                    login_info = None  # todo
                    g.login_member = login_info
                    g.login_id = login_info.get('id', 0) if login_info else  0

                # 字段检查
                if validate_rule:
                    params = request.args if request.method == 'GET' else request.get_json()
                    if params is None:
                        raise ErrArgs
                    do_fields_validate(params, validate_rule)

                response = func(*args, **kwargs)
            except BizError, e:
                return json_response(code=e.code, message=e.message, data=e.data)
            return response

        return do_check
    return handle_func


def do_fields_validate(params, validate_rules):
    """ 字段验证
    :param params:
    :param validate_rules:
    ::

        validate_rules: 两种格式,
        1.list = ['username', 'password']
            字段名称: 都是必须非空的
        2.dict = {'name': ['a', 'min-2', 'max-20', 'email']}
            key: 字段名称
            value: 字段的要求
            value验证规则:
                a = 允许为'',
                min-2 =长度不能少于2
                max-20 =长度不能超过20
                email =邮箱
                phone =手机
                ...
    :return:
    """
    errors = []
    ret_params = {}
    if isinstance(validate_rules, list):
        # 验证规则是list
        for name in validate_rules:
            value = params.get(name)
            if value is None or value == '':
                # 必填非空
                errors.append({'name': name, 'message': u'{}是必填非空项'.format(name)})
            ret_params[name] = value
    else:
        # 验证规则是dict
        for name, validators in validate_rules.items():
            value = params.get(name)
            # 基本验证, 有'r', 则必填
            if 'r' in validators or 'require' in validators:
                if value is None:
                    errors.append({'name': name, 'message': u'{}是必填项'.format(name)})

            if 'n' in validators or 'not-empty' in validators:
                if '' == value:
                    errors.append({'name': name, 'message': u'{}是非空项'.format(name)})

            # 基本验证通过后, 字段开始开始验证
            for validator in validators:
                if validator.startswith('min-'):
                    # 最少长度
                    min_len = int(validator.split('-')[1])
                    if value and len(value) < min_len:
                        errors.append({'name': name, 'message': u'{}长度最少不能少于{}'.format(name, min_len)})
                elif validator.startswith('max-'):
                    # 最大长度
                    max_len = int(validator.split('-')[1])
                    if value and len(value) > max_len:
                        errors.append({'name': name, 'message': u'{}长度最大不能超过{}'.format(name, max_len)})
                elif validator in ('email', 'e'):
                    # 邮箱(murphy.cong-c@i-modou.com.cn)
                    if value and not re.match(r"^(\w)+((\w)*(\.|\-)*(\w)*)*(\w)+@(\w)+(\-)*(\w)+((\.\w+)+)$", value):
                        errors.append({'name': name, 'message': u'{}不是一个正确的邮箱地址'.format(name)})
                elif validator in ('phone', 'p'):
                    # 手机
                    if value and not re.match(r"1\d{10}", value):
                        errors.append({'name': name, 'message': u'{}不是一个正确的手机号码'.format(name)})
            # 验证通过
            ret_params[name] = value
    # 传入的参数加入g
    g.params = ret_params
    # 如果有错误, 抛出业务异常
    if len(errors) != 0:
        message = ', '.join([e.get('message') for e in errors])
        ErrArgs.message = message
        ErrArgs.data = errors
        raise ErrArgs
    return ret_params
