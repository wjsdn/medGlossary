import requests
from bs4 import BeautifulSoup as bs
import re


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)  # 读取网页
        r.raise_for_status()  # 判断网络连接的状态
        r.encoding = 'utf-8'  # 编码方式
        return r.text  # 返回文本数据
    except:
        return ""


def getSentence(html):
    # print(html)
    html = getHTMLText(html)
    soup = bs(html, "html.parser")
    linkre1 = re.compile('href=\"(.+?)\"')  # 获取论文网站链接的正则表达式
    linkre2 = re.compile('</span>(.+?)<span class=\"gs_fl\">')  # 获取例句的正则表达式
    p1 = soup.find('div', id='container').find_all('a')  # 寻找所有此标签
    p2 = soup.find('div', id='container').find_all()  # 寻找所有此标签
    # print(p2)
    links1 = linkre1.findall(str(p1))  # 在此标签内寻找链接
    links2 = linkre2.findall(str(p2))  # 在此标签内寻找链接
    # print(links2)
    links = []
    for i in range(int(len(links1) / 3)):
        links.append(links1[3 * i + 1].replace('amp;', ''))
    sentences = []
    for j in range(int(len(links2) / 3)):
        sentences.append(links2[3 * j + 1].replace('<b>...</b>', '').replace('<br>', '\t').replace('<br/>', '').replace('<b>', '').replace('</b>', '').replace('« PreviousNext »', ''))
    # print(links1)
    # print(links)
    return sentences, links


def main():
    html = "https://www.letpub.com.cn/index.php?page=internal-medicine&med_id=3327&class_id=5"
    sen, link = getSentence(html)
    for i in range(len(sen)):
        print(i,":",sen[i],'\n',link[i])


if __name__ == "__main__":
    main()
