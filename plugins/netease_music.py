import os, re, json, time
import binascii, base64
from Crypto.Cipher import AES

modulus = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
           'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
           '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
           '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
           '3ece0462db0a22b8e7')
nonce = '0CoJUm6Qyw8W8jud'
pubKey = '010001'


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + chr(pad) * pad
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    return ciphertext


def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16), int(pubKey, 16), int(modulus, 16))
    return format(rs, 'x').zfill(256)


def encrypted_request(text):
    text = json.dumps(text)

    secKey = binascii.hexlify(os.urandom(16))[:16]
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    return {'params': encText, 'encSecKey': encSecKey}


class Site:
    name = '网易云音乐'
    domain = '163.com'
    headers = """Host:music.163.com
Origin:http://music.163.com
Referer:http://music.163.com/
User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"""

    def __init__(self, *args):
        self.get, self.post = args[:2]

    def check(self):
        soup = self.get('http://music.163.com/')
        for l in soup.text.splitlines():
            if l.startswith('var GUser='):
                if l == 'var GUser={};':
                    print('\t用户登陆状态失效')
                    return False
                else:
                    l = {k: v for k, v in re.findall(r"[{,]([a-zA-Z]*):[\"]*([^,\}\"]*)[\"]*", l)}
                    print(f'\t用户ID {l["userId"]} 用户名 {l["nickname"]}')
                    # TODO 获得当前是否已经签到, 若已签到便绕过
                    return True

    def process(self):
        r1 = self.post(f'http://music.163.com/weapi/point/dailyTask',
                       encrypted_request({'type': 0}))
        if r1['code'] == 200:
            print(f'\t移动端签到成功 point {r1["point"]}')
        else:
            print(f'\t{r1}')
        time.sleep(0.5)
        r2 = self.post(f'http://music.163.com/weapi/point/dailyTask',
                       encrypted_request({'type': 1}))
        if r2['code'] == 200:
            print(f'\tPC端签到成功 point {r2["point"]}')
        else:
            print(f'\t{r2}')

        ok = [-2, 200]
        if r1['code'] in ok and r2['code'] in ok:
            return True
        else:
            return False
