# 基础返回格式


def BaseResponse(code, msg, data, status=None, err=None):
    result = {
        "code": code,
        "status": status,
        "msg": msg,
        "error": err,
        "data": data
    }
    return result
