import json

"""
    Convert the body of a request into JSON.
"""
def toJSON(body):
    body_unicode = body.decode('utf-8')
    return json.loads(body_unicode)
