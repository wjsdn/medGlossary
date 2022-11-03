from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import os
import xlwt

base_url = 'https://www.letpub.com.cn/index.php?page=med_english&class_id='


def medVocab(j):
    url = base_url + str(j)
    print(url)
    html = urlopen(url).read().decode('utf-8')
    soup = BeautifulSoup(html)
    # soup = BeautifulSoup(html, features='lxml')
    for k in soup.find('div', id='content').find_all('a'):
        name = k.text.strip()

        # worksheet = writer.sheets['Sheet1']  # 默认创建的表格的工作簿名为Sheet1，若不需要进行openpyxl操作，可不写
        f = open('medicalName.txt', 'a', encoding='utf-8')
        f.write(name)
        f.write('\n')
        writer = pd.ExcelWriter('medicalName.xlsx', engine='openpyxl')


def medTaxon():
    html = urlopen(base_url).read().decode('utf-8')
    soup = BeautifulSoup(html)
    for k in soup.find('li').find_all('a'):
        taxon = k.text.strip()
        f = open('medicalName.txt', 'a', encoding='utf-8')
        f.write(taxon)
        f.write('\n')


if __name__ == '__main__':
    medVocab(3)  # 传染病学名词
    medVocab(5)  # 儿童医学名词
    medVocab(6)  # 内科学专业名词
