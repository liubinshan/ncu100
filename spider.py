import requests
from bs4 import BeautifulSoup
from response import Success, Error, validData
import re


class Bs:
    """
    基类，用于创建BeautifulSoup对象
    """

    def __init__(self, url):
        r = requests.get(url=url)
        r.encoding = "utf-8"
        self.bs = BeautifulSoup(r.text, "html.parser")


class GetList(Bs):
    """
    获取文章列表类
    """

    def __init__(self, url, page=1):
        self.page = page
        if self.page > 1:
            url = url[:-4] + "{0:s}".format(str(page - 1)) + url[-4:]
        self.baseUrl = '/'.join(url.split('/')[:-1]) + '/'
        super().__init__(url)

    @validData(Error(400, "访问失败"), Success(200, "访问成功"))
    def getlist(self):
        """
        :return: 一个列表，列表的子项是字典{title:"", time:"", url:"", }
        """
        result = {}
        data = []
        try:
            newDiv = self.bs.find('div', class_='Newslist')
            # 获取页数及文章的总数
            a = newDiv.find('div', attrs={"align": "center"})
            pageAndCount = re.findall(r"\d{1,5}", a.text)  # 利用正则匹配，第一项为文章数， 第二项为页数
            result["page"] = int(pageAndCount[1])
            result["count"] = int(pageAndCount[0])
            # 获取文章的标题、时间、url
            titleAndTime = newDiv.find_all('li', id="line_u8_0")
            for i in titleAndTime:
                time = i.find('span').text
                title = i.find('a').text
                # 处理url
                url = i.find('a').get('href').replace(' ', '')
                if url[0:4] == 'http':
                    pass
                else:
                    url = self.baseUrl + i.find('a').get('href').replace(' ', '')
                data.append({'time': time, 'title': title, 'url': url})
            result['data'] = data
        except Exception as e:
            raise e
        return result


class GetImageList(Bs):
    """
    获取带图片的文章列表类（历史记录）
    """

    def __init__(self, url):
        super().__init__(url)

    @validData(Error(400, "访问失败"), Success(200, "访问成功"))
    def getimagelist(self):
        data = []
        result = {}
        try:
            newDiv = self.bs.find('div', class_='Newslist')
            titleAndImage = newDiv.find_all('a')
            for i in titleAndImage:
                title = i.find('p').text
                # 处理图片链接
                imageurl = i.find('img').get('src').replace(' ', '')
                if imageurl[0:4] == 'http':
                    pass
                else:
                    imageurl = "http://100.ncu.edu.cn/" + imageurl[6:]
                data.append({'title': title, 'imageurl': imageurl})
            result['data'] = data
        except Exception as e:
            raise e
        return result


class GetContent(Bs):
    """
    获取文章内容的类
    """

    def __init__(self, url):
        super().__init__(url)

    @validData(Error(400, "访问失败"), Success(200, "访问成功"))
    def getcontent(self):
        """
        :return: 一个字典，
        """
        result = {}
        try:
            titleDiv = self.bs.find('div', class_="content-title")
            conDiv = self.bs.find('div', class_="content-con")
            # 获取标题
            title = titleDiv.find('h3').text
            # 获取时间
            time = re.findall(r'\d{1,4}-\d{1,2}-\d{1,2}', titleDiv.find('i').text)
            # 得到内容
            cons = conDiv.contents[1:-1]
            content = ''
            # 对内容进行拼接
            for i in cons:
                content = content + str(i)
            data = {'title': title, 'time': time[0], 'content': content}
            result["data"] = data
        except Exception as e:
            raise e
        return result


class GetNavList(Bs):
    """
    获取校庆网站的导航栏内容的类
    """

    def __init__(self, url):
        super().__init__(url)

    @validData(Error(400, "访问失败"), Success(200, "访问成功"))
    def getnavlist(self):
        """
        :return:一个字典，键为相应网页的标题，值为对应的url
        """
        titledir = {}
        left = self.bs.find("div", class_="nav fl")
        right = self.bs.find("div", class_="nav1 fr")
        leftItem = left.find_all("a")
        rightItem = right.find_all("a")
        allItem = leftItem + rightItem
        for item in allItem:
            name = item.text
            url = 'http://100.ncu.edu.cn/' + item.get('href').replace(' ', '')  # 去除url中的空格，并将url进行拼接
            titledir[name] = url
        return titledir


if __name__ == "__main__":
    l = GetList('')
    print(l.getlist())
