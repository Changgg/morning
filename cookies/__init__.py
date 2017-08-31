import os, json

__dir__ = os.path.dirname(__file__)


class Cookies:
    def __init__(self, domain):
        self.domain = domain
        self.path = f"{os.path.join(__dir__, self.domain)}.txt"

    def __bool__(self):
        return os.path.exists(self.path)

    def __iter__(self):
        if self:
            try:
                with open(self.path) as f:
                    c = json.load(f)
            except:
                raise NotImplementedError('cookies 格式不支持')
            else:
                for c in c:
                    yield c['name'], c['value']
