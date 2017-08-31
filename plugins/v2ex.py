import re


class Site:
    name = 'V2EX'
    domain = 'v2ex.com'

    def __init__(self, *args):
        self.balance = {}
        self.get, self.post = args[:2]

    def check(self):
        soup = self.get('https://www.v2ex.com/mission/daily')
        if soup.title.text.endswith('登录'):
            print('\t登录状态失效')
            return False
        uid = soup.select_one('#Top a[href^=/member/]')
        if not uid:
            return False
        uid = uid.text if uid.text == uid['href'][8:] else None
        if not uid:
            return False

        notification = soup.select_one('a[href=/notifications]')
        if not notification:
            return False
        notification = notification.text

        balance = soup.select_one('#money .balance_area')
        if not balance:
            return False
        i = 0
        for t in balance.contents:
            try:
                t = t.title().strip()
                if t:
                    i = int(t)
            except:
                self.balance[t['alt']] = i
        soup.select('#money')

        print(f"""\t用户ID {uid}\t{notification}\t{self.balance}""")

        if not "每日登录奖励已领取" in soup.text:
            once = re.findall(r"\/mission\/daily\/redeem\?once=(.*)\'",
                              soup.select_one('input[onclick^=location.href]')['onclick'])
            once = int(once[0]) if once else None
            if once:
                self.once = once
            else:
                print('\tonce 没有提取到')
                return False
        return True

    def process(self):
        if not hasattr(self, 'once'):
            print('\t重复签到')
            return True
        soup = self.get(f'https://www.v2ex.com/mission/daily/redeem?once={self.once}')
        if '已成功领取每日登录奖励' in soup.text:
            print('\t签到成功')
            return True
        else:
            print('\t请求已提交但返回结果未知')
