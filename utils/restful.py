from flask import jsonify


class HttpCode(object):
    ok = 200
    unloginerror = 401
    permissionerror = 403
    paramserror = 400
    servererror = 500


def _restful_result(code, message, data):
    return jsonify({"message": message or "", "data": data or {}, "code": code})


def ok(message=None, data=None):
    return _restful_result(code=HttpCode.ok, message=message, data=data)


def unlogin_error(message="没有登录"):
    return _restful_result(code=HttpCode.unloginerror, message=message, data=None)


def permission_error(message="没有访问权限"):
    return _restful_result(code=HttpCode.permissionerror, message=message, data=None)


def params_error(message="参数错误"):
    return _restful_result(code=HttpCode.paramserror, message=message, data=None)


def server_error(message="服务器开小差啦"):
    return _restful_result(code=HttpCode.servererror, message=message or '服务器内部错误', data=None)
