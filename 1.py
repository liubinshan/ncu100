import requests
import random
import os
from getip import getip
from bs4 import BeautifulSoup
from tqdm import tqdm


# ����ҳ�����ȡִ��һ���Ĳ���
# ��ȡһ����ҳ�����ݲ�����
def savemsg(targetUrl, iplist, savedir):
    """

    :param targetUrl: Ҫ��ȡ��վ����ַ
    :param iplist: һ���б��������ֵ�,��Ϊ��http��,ֵΪip��ַ
    :param savedir: ��ҳ���ݴ�ŵ�Ŀ¼
    :return: None
    """
    re = requests.get(url=targetUrl, headers=header, proxies=random.choice(ipList))
    re.encoding = 'utf-8'
    bs = BeautifulSoup(re.text, 'html.parser')
    imgList = bs.find_all("img")
    if imgList != None:
        # ������ַ��ʼ��ȡͼƬ
        imgUrls = []
        imgnames = []
        # ����ͼƬ��ŵ��ļ���
        saveDir = os.path.join(savedir, 'image')
        checkSaveDir(saveDir)
        for i in tqdm(imgList):
            imgname = i.get('src')[6:]
            imgUrl = "http://100.ncu.edu.cn/" + i.get('src')
            imgnames.append(imgname)
            # ��ʼ��ȡͼƬ
            imgUrls.append(imgUrl)
            savePath = saveDir + imgname
            response = requests.get(imgUrl, headers=header, proxies=random.choice(ipList))
            if response.status_code == 200:
                with open(savePath, 'wb') as f:
                    f.write(response.content)
            else:
                print(imgUrl)
                print("����ʧ��")
        # ��ʼ��ȡ�ı�
        n = bs.find('div', class_="Newslist")



# ����ļ����Ƿ����
def checkSaveDir(savedir):
    if os.path.exists(savedir):
        os.mkdir(saveDir)
    else:
        pass


# ��ȡip
ipList = getip()

# saveDir = input("������Ҫ������ļ�����:")
saveDir = "����У��"
baseDir = os.path.join(os.getcwd(), saveDir)  # baseDir��ŵ�ǰ�ļ��е�·��
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
urlList = []  # ��������Ҫ���ʵ���������
names = []
# ��������
for i in aList:
    names.append(i.text)
    urlList.append(i.get('href'))
print(urlList)
print(names)
# ����ַƴ�ӳɿ��Է��ʵ���ַ
for i in range(1, len(urlList)):
    # ȥ�������еĿո�
    if ' ' in urlList[i]:
        urlList[i] = urlList[i].replace(' ', '')
    urlList[i] = "http://100.ncu.edu.cn/" + urlList[i]
print(urlList)
# ȥ�������еĿո�
for i in range(0, len(names)):
    if " " in names[i]:
        names[i] = names[i].replace(' ', '')

print(names)

# ���ɵ�ǰҳ��ͼƬ���Ӳ���ȡҳ���ͼƬ
imgUrls = []
imgnames = []
saveDir = os.path.join(saveDir, 'image')
checkSaveDir(saveDir)
for i in tqdm(imgList):
    imgname = i.get('src')[6:]
    imgUrl = "http://100.ncu.edu.cn/" + i.get('src')
    imgnames.append(imgname)
    # ��ʼ��ȡ��ҳͼƬ
    imgUrls.append(imgUrl)
    savePath = saveDir + imgname
    response = requests.get(imgUrl, headers=header, proxies=random.choice(ipList))
    if response.status_code == 200:
        with open(savePath, 'wb') as f:
            f.write(response.content)
    else:
        print(imgUrl)
        print("����ʧ��")
# ��ȡ��ҳ���ı�
for i in tqdm(range(1, len(names))):
    if len(names[i]) != 4 and len(names[i]) != 0:
        # ���ñ����ļ���
        # saveDir = os.path.join(saveDir, r'../')
        # ���ñ���·�����ļ���
        savePath = saveDir + '/' + names[i] + '.txt'
        response = requests.get(url=urlList[i], headers=header, proxies=random.choice(ipList))
        response.encoding = 'utf-8'
        if response.status_code == 200:
            bs = BeautifulSoup(response.text, "html.parser")
            # ��ȡ��������
            con = bs.find('div', class_='content-title')
            if con != None:
                title = con.find_all('h3')
                t = con.find_all('i')
            # ��ȡ��������
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
            print("����ʧ��")
# ��ʼ��ȡ��ҳ��
# ���ڵ�һ����ַ�͵ڶ�����ַ�ֱ�Ϊ�ϲ���ѧ��������ҳ������������
# ���ñ����ļ���
for i in range(2, len(names)):
    if names[i] == 4:
        # �����ļ���
        saveDir = os.path.join(baseDir, names[i])
        checkSaveDir(saveDir)
        re = requests.get(url=urlList[i], headers=header, proxies=random.choice(ipList))
        re.encoding = 'utf-8'
        bs = BeautifulSoup(re.text, 'html.parser')
        imgList = bs.find_all("img")
        # ������ַ��ʼ��ȡ����
        imgUrls = []
        imgnames = []
        # ����ͼƬ��ŵ��ļ���
        saveDir = os.path.join(saveDir, 'image')
        checkSaveDir(saveDir)
        for i in tqdm(imgList):
            imgname = i.get('src')[6:]
            imgUrl = "http://100.ncu.edu.cn/" + i.get('src')
            imgnames.append(imgname)
            # ��ʼ��ȡͼƬ
            imgUrls.append(imgUrl)
            savePath = saveDir + imgname
            response = requests.get(imgUrl, headers=header, proxies=random.choice(ipList))
            if response.status_code == 200:
                with open(savePath, 'wb') as f:
                    f.write(response.content)
            else:
                print(imgUrl)
                print("����ʧ��")
        # ��ʼ��ȡ�ı�
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