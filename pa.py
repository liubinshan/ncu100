import requests
import random
import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import json

url = "http://100.ncu.edu.cn/xshd/159855ca0f2d4029ae24fef823c69909.htm"

re = requests.get(url=url)
re.encoding = 'utf-8'
bs = BeautifulSoup(re.text, "html.parser")
con = bs.find("div", class_="content-con")
print(str(con.contents[1]))
content = {}
content["content"] = str(con.contents[1])
print(json.dumps(content, ensure_ascii=False))
