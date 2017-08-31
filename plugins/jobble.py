import re


class Site:
    name = '伯乐在线'
    domain = 'jobbole.com'

    def __init__(self, *args):
        self.balance = {}
        self.get, self.post = args[:2]

    def check(self):
        soup = self.get('http://www.jobbole.com/')
        urlprefix = "http://www.jobbole.com/members/"
        uid = soup.select_one(f'#menu-main-menu a[href^={urlprefix}]')
        if uid:
            uid = uid['href'][len(urlprefix):]
            if uid:
                print(f"""\t用户ID {uid}""")
                return True
        return False

    def process(self):
        r = self.post('http://www.jobbole.com/wp-admin/admin-ajax.php', data=dict(action='get_login_point'))
        print(f'\t返回结果 {r}')
        if r['jb_result'] in [-1]:
            return True
        return False
