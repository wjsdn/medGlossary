import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import re
import xlwt
import os


def main():
    url = 'https://www.letpub.com.cn/index.php?page=med_english&class_id='
    html = getHTMLText(url)  # 获取网站页面
    # writeTaxon(html)  # 提取各个分类的网站
    makepath = "medGlossary"  # 创建文件夹
    s = [4, 5]
    writeXls(makepath, html, s)


'''(1)获取网站页面'''


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)  # 读取网页
        r.raise_for_status()  # 判断网络连接的状态
        r.encoding = 'utf-8'  # 编码方式
        return r.text  # 返回文本数据
    except:
        return ""


'''(2)创建表格路径'''


def mkdir(path):  # 创建表格所在目录
    path = path.strip()  # 去除首位空格
    path = path.rstrip("\\")  # 去除尾部\符号
    # 判断目录路径是否存在，若存在为True，若不存在为False
    ifExists = os.path.exists(path)
    if not ifExists:
        # 如果不存在则创建此目录
        os.makedirs(path)
        return True
    else:
        # 如果此目录存在则不创建
        return False


'''(3)提取各个分类名和对应链接'''


def getTaxon(html):
    soup = bs(html, "html.parser")
    linkre1 = re.compile('href=\"(.+?)\"')  # 获取分类网站链接的正则表达式
    p = soup.find('div', id={'container'}).find_all('li')  # 寻找所有li标签
    links = linkre1.findall(str(p))  # 在li标签内寻找链接
    # print(links)
    for i in range(len(links)):
        links[i] = links[i].replace('amp;', '')  # 去掉"amp;"
        links[i] = 'https://www.letpub.com.cn/' + links[i]  # 补齐网址，使成为可以直接访问的地址
    linkre2 = re.compile('[\u4e00-\u9fa5]+?-中英文词汇翻译')
    taxons = linkre2.findall(str(p))  # 在li标签内寻找分类名称
    for i in range(len(taxons)):
        taxons[i] = taxons[i][:-8]
    return taxons, links


def selectTaxon(t, l, s):
    taxons, links = [], []
    for i in range(len(s)):
        taxons.append(t[s[i]])
        links.append(l[s[i]])
    return taxons, links


'''(4)记录各个分类的网站到txt文件中'''


def writeTaxon(html):
    names, links = getTaxon(html)
    file = open("links.txt", "w")  # 网址存在“links.txt”文件中
    for i in range(len(names)):
        # print(names[i] + '：' + links[i])
        file.write(names[i] + '：' + links[i] + '\n')  # 将分类名称和相应链接写入创建好的文档中


'''(5)爬取某分类所有词条的中英形式及其例句链接'''


def getWord(html):
    html = getHTMLText(html)
    soup = bs(html, "html.parser")
    linkre = re.compile('href=\"(.+?)\"')  # 获取例句网站链接的正则表达式
    p = soup.find('div', id={'content'}).find_all('a')  # 寻找所有此标签
    links = linkre.findall(str(p))  # 在此标签内寻找链接
    for i in range(int(len(links) / 2)):
        links[i] = links[2 * i].replace('amp;', '')  # 去掉"amp;"
        links[i] = 'https://www.letpub.com.cn/' + links[i]  # 补齐网址，使成为可以直接访问的地址
    words = []
    for k in p:
        words.append(k.text.strip())
    ch, en = [], []
    for i in range(int(len(words) / 2)):
        ch.append(words[2 * i])
        en.append(words[2 * i + 1])
    return ch, en, links


'''(6)爬取某词条所有例句及其论文链接'''


def getSentence(html):
    # print(html)
    html = getHTMLText(html)
    soup = bs(html, "html.parser")
    linkre1 = re.compile('href=\"(.+?)\"')  # 获取论文网站链接的正则表达式
    linkre2 = re.compile('target=\"_blank\">(.+?)</a>')  # 获取例句的正则表达式
    p1 = soup.find('div', id='container')  # 寻找所有此标签
    if p1:
        p1 = p1.find_all('h3')  # 寻找所有此标签
    p2 = soup.find('div', id='container')  # 寻找所有此标签
    if p2:
        p2 = p2.find_all('h3')  # 寻找所有此标签
    # print(len(p2))
    # print(p2)
    links1 = linkre1.findall(str(p1))  # 在此标签内寻找链接
    links2 = linkre2.findall(str(p2))  # 在此标签内寻找链接
    # print(links2)
    links = []
    for i in range(len(links1)):
        links.append(links1[i].replace('amp;', ''))
    sentences = []
    for j in range(len(links2)):
        # print(links1)
        sentences.append(
            links2[j].replace('<b>...</b>', '').replace('<br>', '\t').replace('<br/>', '').replace('<b>', '').replace(
                '</b>', ''))
    # print(links)
    # print(len(sentences))
    # print(sentences)
    return sentences, links


'''(7)存入表格'''


def writeXls(file, link, s):
    mkdir(file)
    taxon_name, word_link = getTaxon(link)
    taxon_name, word_link = selectTaxon(taxon_name, word_link, s)
    # print(len(taxon_name), word_link[0])
    # cn, en, sentence_link = getWord(word_link[0])

    if not os.path.exists("medGlossary\\words1.xls"):  # 不存在则创建
        w1 = xlwt.Workbook()
        sheet1 = w1.add_sheet("words")  # 工作表
        sheet1.write(0, 0, "词条")
        sheet1.write(0, 1, "释义")
        sheet1.write(0, 2, "音标")
        sheet1.write(0, 3, "词性")
        sheet1.write(0, 4, "分类")
        sheet2 = w1.add_sheet("sentences")  # 工作表
        sheet2.write(0, 0, "词条")
        sheet2.write(0, 1, "论文题目")
        sheet2.write(0, 2, "论文链接")
        row, row1, row2 = 0, 0, 0
        for i in range(len(taxon_name)):
            # print(len(taxon_name), word_link[i])
            cn, en, sentence_link = getWord(word_link[i])
            # print(cn)
            # print(en)
            for j in range(len(en)):
                sheet1.write(j + 1 + row, 0, en[j])  # (j+1,0)写入词条
                sheet1.write(j + 1 + row, 1, cn[j])  # (j+1,1)写入释义
                sheet1.write(j + 1 + row, 4, taxon_name[i])  # (j+1,4)写入分类
                # print(row)
                sentence, thesis_link = getSentence(sentence_link[j])
                # print(thesis_link)
                l = min(len(sentence), len(thesis_link))
                if sentence: sheet2.write(1 + row1 + row, 0, en[j])
                for k in range(l):
                    sheet2.write(k + 1 + row1 + row, 1, sentence[k])
                    sheet2.write(k + 1 + row1 + row, 2, thesis_link[k])
                row1 += l
            row += len(en)
        alignment = xlwt.Alignment()  # 设置对齐方式
        alignment.horz = xlwt.Alignment.HORZ_LEFT
        alignment.vert = xlwt.Alignment.VERT_CENTER
        w1.save("medGlossary\\words1.xls")


if __name__ == '__main__':
    main()
