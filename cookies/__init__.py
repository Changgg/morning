import os, json

import requests
import browsercookie

__dir__ = os.path.dirname(__file__)


class Cookies:
    def __init__(self, domain):
        self.domain = domain
        self.jar = None
        self.path = f"{os.path.join(__dir__, self.domain)}.txt"
        if self:
            try:
                with open(self.path) as f:
                    c = json.load(f)
            except:
                raise NotImplementedError('cookies 格式不支持')
            else:
                self.jar = requests.utils.cookiejar_from_dict({c['name']: c['value'] for c in c})
        else:  # 文件不存在便尝试从浏览器中读取
            self.jar = browsercookie.firefox()

    def __bool__(self):
        return os.path.exists(self.path)
