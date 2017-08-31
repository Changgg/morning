import os, json

__dir__ = os.path.dirname(__file__)


class Cookies:
    def __init__(self, domain):
        self.domain = domain
        self._cookies = {}
        self.path = f"{os.path.join(__dir__, self.domain)}.txt"
        if self:
            try:
                with open(self.path) as f:
                    c = json.load(f)
            except:
                raise NotImplementedError('cookies 格式不支持')
            else:
                for c in c:
                    self._cookies[c['name']] = c['value']
        else:  # 文件不存在便尝试从浏览器中读取
            pass

    def __bool__(self):
        return os.path.exists(self.path)

    def __iter__(self):
        for k, v in {}.items():
            yield k, v
