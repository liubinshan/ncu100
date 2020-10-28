import requests
from bs4 import BeautifulSoup
import time


# 验证爬取的ip是否可用
def testip(testUrl):
    url = "http://www.baidu.com/"
    try:
        res = requests.get(url=url, proxies=testUrl, timeout=5)
        # 成功
        if res.status_code == 200:
            return True
    except Exception as e:
        return False


def getip(num=1):
    """

    :return: 一个列表，里面是字典,键为“http“,值为ip地址
    """
    hearder = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"}
    ipList = []
    for n in range(0, num):
        r = requests.get("https://www.kuaidaili.com/free/inha/", headers=hearder)
        target = r.text
        bs = BeautifulSoup(target, 'html.parser')
        # 找到ip
        ip1 = bs.find_all('td', attrs={'data-title': "IP"})
        # 找到ip的端口
        ip2 = bs.find_all('td', attrs={'data-title': "PORT"})
        # 找到ip的类型
        ipN = bs.find_all('td', attrs={'data-title': "匿名度"})
        # 找到ip的协议
        ipType = bs.find_all('td', attrs={'data-title': "类型"})
        ip = {}
        for i in range(0, len(ip1)):
            ip[ipType[i].text] = ip1[i].text + ':' + ip2[i].text
            if testip(ip):
                ipList.append({ipType[i].text: ip[ipType[i].text]})
        time.sleep(2)
    return ipList


if __name__ == "__main__":
    print(getip(5))
