import json


def toJSON(body):
    body_unicode = body.decode('utf-8')
    return json.loads(body_unicode)
