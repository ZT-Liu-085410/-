# 采用百度翻译
import requests
import random
import hashlib
import time

APP_ID = '20250624002389404'
SECRET_KEY = 'kAd7zw1Zt6FqX8YMIRI_'

def baidu_translate(text, from_lang='zh', to_lang='en', retries=3):
    api_url = 'https://fanyi-api.baidu.com/api/trans/vip/translate'
    for i in range(retries):
        try:
            salt = str(random.randint(32768, 65536))
            sign_str = APP_ID + text + salt + SECRET_KEY
            sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

            params = {
                'q': text,
                'from': from_lang,
                'to': to_lang,
                'appid': APP_ID,
                'salt': salt,
                'sign': sign
            }

            response = requests.get(api_url, params=params, timeout=5)
            result = response.json()

            if 'trans_result' in result:
                return result['trans_result'][0]['dst']
            else:
                print(f"翻译接口错误，返回：{result}")
                time.sleep(1)
        except Exception as e:
            print(f"翻译异常，尝试第{i+1}次，错误：{e}")
            time.sleep(1)
    return "【翻译失败】"
