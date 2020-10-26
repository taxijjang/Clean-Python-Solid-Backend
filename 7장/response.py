import json


class Response:
    def __init__(self, status=200, code='OK', data=None):
        self.status = status
        self.code = code
        self.data = data

    def __call__(self, *args, **kwargs):
        print( {
                'status' : self.status,
                'code' : self.code,
                'data': self.data
            })
