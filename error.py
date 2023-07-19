class StatusError(Exception):
    def __init__(self, message, error_code=None, url=None):
        self.message = message
        self.error_code = error_code
        self.url = url

    def to_dict(self):
        error_dict = {
            'message': self.message,
        }
        if self.error_code is not None:
            error_dict['error_code'] = self.error_code
        if self.url is not None:
            error_dict['url'] = self.url
        return error_dict
    
class UrlError(Exception):
    def __init__(self, message, url=None):
        self.message = message
        self.url = url

    def to_dict(self):
        error_dict = {
            'message': self.message,
        }
        if self.url is not None:
            error_dict['url'] = self.url
        return error_dict