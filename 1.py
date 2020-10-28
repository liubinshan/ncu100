import requests
import random
import os
from getip import getip
from bs4 import BeautifulSoup
from tqdm import tqdm


# 所有页面的爬取执行一样的操作
# 爬取一个网页的内容并保存
def savemsg(targetUrl, iplist, savedir):
    """

    :param targetUrl: 要爬取网站的网址
    :param iplist: 一个列表，里面是字典,键为“http“,值为ip地址
    :param savedir: 网页内容存放的目录
    :return: None
    """
    re = requests.get(url=targetUrl, headers=header, proxies=random.choice(ipList))
    re.encoding = 'utf-8'
    bs = BeautifulSoup(re.text, 'html.parser')
    imgList = bs.find_all("img")
    if imgList != None:
        # 进入网址开始爬取图片
        imgUrls = []
        imgnames = []
        # 创建图片存放的文件夹
        saveDir = os.path.join(savedir, 'image')
        checkSaveDir(saveDir)
        for i in tqdm(imgList):
            imgname = i.get('src')[6:]
            imgUrl = "http://100.ncu.edu.cn/" + i.get('src')
            imgnames.append(imgname)
            # 开始爬取图片
            imgUrls.append(imgUrl)
            savePath = saveDir + imgname
            response = requests.get(imgUrl, headers=header, proxies=random.choice(ipList))
            if response.status_code == 200:
                with open(savePath, 'wb') as f:
                    f.write(response.content)
            else:
                print(imgUrl)
                print("连接失败")
        # 开始爬取文本
        n = bs.find('div', class_="Newslist")



# 检查文件夹是否存在
def checkSaveDir(savedir):
    if os.path.exists(savedir):
        os.mkdir(saveDir)
    else:
        pass


# 获取ip
ipList = getip()

# saveDir = input("请输入要保存的文件夹名:")
saveDir = "百年校庆"
baseDir = os.path.join(os.getcwd(), saveDir)  # baseDir存放当前文件夹的路径
checkSaveDir(baseDir)
targetUrl = "http://100.ncu.edu.cn/"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"}
req = requests.get(targetUrl, headers=header, proxies=random.choice(ipList))
req.encoding = 'utf-8'
bs = BeautifulSoup(req.text, "html.parser")
aList = bs.find_all('a')
imgList = bs.find_all('img')
print(aList)
print(imgList)
urlList = []  # 用来放置要访问的所有链接
names = []
# 生成链接
for i in aList:
    names.append(i.text)
    urlList.append(i.get('href'))
print(urlList)
print(names)
# 将网址拼接成可以访问的网址
for i in range(1, len(urlList)):
    # 去掉链接中的空格
    if ' ' in urlList[i]:
        urlList[i] = urlList[i].replace(' ', '')
    urlList[i] = "http://100.ncu.edu.cn/" + urlList[i]
print(urlList)
# 去掉名字中的空格
for i in range(0, len(names)):
    if " " in names[i]:
        names[i] = names[i].replace(' ', '')

print(names)

# 生成当前页面图片链接并爬取页面的图片
imgUrls = []
imgnames = []
saveDir = os.path.join(saveDir, 'image')
checkSaveDir(saveDir)
for i in tqdm(imgList):
    imgname = i.get('src')[6:]
    imgUrl = "http://100.ncu.edu.cn/" + i.get('src')
    imgnames.append(imgname)
    # 开始爬取首页图片
    imgUrls.append(imgUrl)
    savePath = saveDir + imgname
    response = requests.get(imgUrl, headers=header, proxies=random.choice(ipList))
    if response.status_code == 200:
        with open(savePath, 'wb') as f:
            f.write(response.content)
    else:
        print(imgUrl)
        print("连接失败")
# 爬取首页的文本
for i in tqdm(range(1, len(names))):
    if len(names[i]) != 4 and len(names[i]) != 0:
        # 设置保存文件夹
        # saveDir = os.path.join(saveDir, r'../')
        # 设置保存路径及文件名
        savePath = saveDir + '/' + names[i] + '.txt'
        response = requests.get(url=urlList[i], headers=header, proxies=random.choice(ipList))
        response.encoding = 'utf-8'
        if response.status_code == 200:
            bs = BeautifulSoup(response.text, "html.parser")
            # 获取标题内容
            con = bs.find('div', class_='content-title')
            if con != None:
                title = con.find_all('h3')
                t = con.find_all('i')
            # 获取文章内容
            contents = bs.find("div", class_='content-con')
            if contents != None:
                contents = contents.find_all('p')
            if con != None and contents != None:
                with open(savePath, "w", encoding='utf-8') as f:
                    try:
                        f.write(title[0].text)
                        f.write('\n')
                        f.write(t[0].text)
                        for c in contents:
                            f.write(c.text)
                            f.write("\n")
                    except Exception as e:
                        pass
        else:
            print(urlList[i])
            print("连接失败")
# 开始爬取子页面
# 由于第一个网址和第二个网址分别为南昌大学官网和首页所以我们跳过
# 设置保存文件夹
for i in range(2, len(names)):
    if names[i] == 4:
        # 创建文件夹
        saveDir = os.path.join(baseDir, names[i])
        checkSaveDir(saveDir)
        re = requests.get(url=urlList[i], headers=header, proxies=random.choice(ipList))
        re.encoding = 'utf-8'
        bs = BeautifulSoup(re.text, 'html.parser')
        imgList = bs.find_all("img")
        # 进入网址开始爬取数据
        imgUrls = []
        imgnames = []
        # 创建图片存放的文件夹
        saveDir = os.path.join(saveDir, 'image')
        checkSaveDir(saveDir)
        for i in tqdm(imgList):
            imgname = i.get('src')[6:]
            imgUrl = "http://100.ncu.edu.cn/" + i.get('src')
            imgnames.append(imgname)
            # 开始爬取图片
            imgUrls.append(imgUrl)
            savePath = saveDir + imgname
            response = requests.get(imgUrl, headers=header, proxies=random.choice(ipList))
            if response.status_code == 200:
                with open(savePath, 'wb') as f:
                    f.write(response.content)
            else:
                print(imgUrl)
                print("连接失败")
        # 开始爬取文本
        tit = bs.find("div", class_="content-title")
        con = bs.find("div", class_="content-con")
        if tit != None:
            title = tit.find_all("h3")
            t = tit.find_all("i")
        if con != None:
            contents = con.find_all("p")
        if tit != None and con != None:
            savePath = saveDir + title[0].text + ".txt"
            with open(savePath, "w", encoding='utf-8'):
                f.write(title[0].text)
                f.write('\n')
                f.write(t[0].text)
                for content in contents:
                    pass