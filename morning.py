import json, os, datetime
import requests
from functools import partial
from faker import Faker
import time
from bs4 import BeautifulSoup

import plugins
from cookies import Cookies
from config import list_black

session = requests.session()
__dir__ = os.path.dirname(__file__)


def http_request(method, *args, count_error=[3], **kwargs):
    if method == 'GET':
        resp = session.get(*args, **kwargs)
    elif method == 'POST':
        resp = session.post(*args, **kwargs)
    else:
        raise NotImplementedError('Not Implemented!!!')

    if resp.status_code == 200:
        count_error[0] = 3
        try:
            c = json.loads(resp.text)
        except ValueError:
            return BeautifulSoup(resp.text, 'lxml')
        else:
            return c

    else:
        count_error[0] -= 1
        if not count_error[0]:
            raise RuntimeError('连续3次网络请求失败')
        time.sleep(1)


if __name__ == '__main__':
    path_logs = os.path.join(__dir__, 'logs.json')
    with open(path_logs, 'r') as file_logs:
        logs = json.load(file_logs)
    for Site in plugins.sites:
        # 自动过滤3小时内成功操作的站点
        d = logs.get(Site.domain, None)
        if d:
            d = datetime.datetime(*d[:6])
            if not (datetime.datetime.now() - d).seconds / (60 * 60 * 6) >= 1:
                continue
        # 黑名单功能（默认启用所用站点）
        if Site.domain not in list_black:
            # 读取Cookies
            c = Cookies(Site.domain)
            if c:
                session.cookies = c.jar
            else:
                session.cookies = requests.utils.cookiejar_from_dict({})
            # 重置请求头
            session.headers = requests.utils.default_headers()
            if hasattr(Site, 'headers'):
                for l in Site.headers.split('\n'):
                    k, v = l.split(':', 1)
                    k, v = k.strip(), v.strip()
                    session.headers[k] = v
            else:
                session.headers['User-Agent'] = Faker().chrome()
            # 创建站点的实例
            s = Site(partial(http_request, 'GET'), partial(http_request, 'POST'))
            print(f'站点 {s.name} {s.domain}')
            s.cookies = session.cookies
            if s.check():  # 站点的登录状态检查
                if s.process():  # 处理站点是否需要执行操作后执行操作
                    logs[s.domain] = list(datetime.datetime.now().timetuple())[:6]
                else:
                    print('\t处理过程出现问题')
                print('')
    with open(path_logs, 'w') as file_logs:
        json.dump(logs, file_logs, sort_keys=True, indent=4)
