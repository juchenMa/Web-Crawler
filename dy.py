# encoding:UTF-8
from bs4 import BeautifulSoup
import lxml
import requests
import pymysql


list1 = []


def getsection():  # 获得各个游戏的href
    url = 'https://www.douyu.com/directory'
    html = requests.get(url).text
    dy = BeautifulSoup(html, 'lxml')
    a = 2

    while a < 10:
        tag1 = dy.section.main.section.contents[a]
        getgamehref(tag1)
        a += 1
    return


def getgamehref(tag):
    str1 = tag.ul.li.a.get('href')
    str2 = 'www.douyu.com'
    str3 = str2 + str1
    list1.append(str3)
    for b in tag.ul.li.next_siblings:
        str1 = b.a.get('href')
        str3 = str2 + str1
        list1.append(str3)
    return


def visitgamerhref():
    url = 'http://'
    a = 0
    while a < len(list1):
        url1 = url + list1[a]
        html = requests.get(url1).text
        dy = BeautifulSoup(html, 'lxml')
        visitperson(dy)
        a += 1
    return


def visitperson (dy1):
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='localhost',
        password='123',
        database='dydata1',
        charset='utf8')

    cursor = conn.cursor()

    individual = dy1.section.main.section.next_sibling.ul.li
    human = individual.div.a.div.next_sibling.div.next_sibling.span.text
    name = individual.div.a.div.next_sibling.div.next_sibling.h2.text
    account = individual.div.a.get('href')

    sql = "INSERT INTO dy (name,hot,account)VALUES (%s,%s,%s);"
    af = 0
    try:
        cursor.execute(sql, (name, human, account))
        conn.commit()
        print('导入成功')
    except Exception as ex:
        print(ex)
        conn.rollback()
        print("导入失败")
        print(name)
        print(human)
        print(account)
    for indi in individual.next_siblings:
        human = indi.div.a.div.next_sibling.div.next_sibling.span.text
        name = indi.div.a.div.next_sibling.div.next_sibling.h2.text
        account = indi.div.a.get('href')
        print(af)
        af += 1
        try:
            cursor.execute(sql, (name, human, account))
            conn.commit()
            print('导入成功')
        except Exception as ex:
            print(ex)
            conn.rollback()
            print("导入失败")
            print(name)
            print(human)
            print(account)
    conn.rollback()
    cursor.close()
    conn.close()
    return




getsection()
visitgamerhref()


