from urllib import request
from bs4 import BeautifulSoup
import re
import pymysql
import time


class Boss():
    # 初始化
    def __init__(self, url, boss_type, n):
        self.url = url
        self.boss_type = boss_type
        self.http = r'https://www.zhipin.com'
        self.n = n
        # 打开数据库连接
        self.db = pymysql.connect("localhost", "root", "root", "pvpmnm", use_unicode=True, charset="utf8")
        # 使用 cursor() 方法创建一个游标对象 cursor
        self.cursor = self.db.cursor()

    # 单页爬取
    def spider(self):
        for j in range(self.n):
            url = self.url + '?page=%d' % (j + 1)
            # 抓取
            with request.urlopen(url) as f:
                html = f.read().decode('utf-8')

            soup = BeautifulSoup(html, 'html.parser')

            lists = soup.find('div', class_='job-list').find_all('li')
            # 解析
            i = 30 * j + 1
            for item in lists:
                # info-primary
                info_primary = item.find('div', class_='job-primary')
                job_name = info_primary.find('div', class_='job-title').text  # 岗位名字
                job_href = self.http + info_primary.find('a').get('href')  # 详情链接
                money = info_primary.find('span', class_='red').text
                money = money.split('-', 1)
                money_min = int((money[0])[0:-1])  # 薪资最小
                money_max = int((money[1])[0:-1])  # 薪资最大
                primary_line = str(info_primary.find_all('p')[1]).split('<em class="vline"></em>', 2)
                address = (primary_line[0])[3:]  # 公司地址
                age = primary_line[1]  # 年限
                certificate = (primary_line[2])[0:-4]  # 学历
                # info-company
                info_company = item.find('div', class_='info-company')
                company_name = info_company.find('a').text  # 公司名字
                company_href = self.http + info_company.find('a').get('href')  # 公司链接
                company_line = (str(info_company.find('p'))).split('<em class="vline"></em>', 2)
                trade = (company_line[0])[3:]  # 行业
                company_round = ''  # 轮次
                # company_round = (company_line[1])  # 轮次

                if (company_line[1])[0:-5]:
                    scale = (company_line[1])[0:-5]  # 规模
                else:
                    scale = (company_line[2])[0:-5]  # 规模
                # info-publish
                info_publish = item.find('div', class_='info-publis')
                publish_href = info_publish.find('img').get('src')  # 发布人头像
                publish_line = (str(info_publish.find('h3'))).split('<em class="vline"></em>', 1)
                re_words = re.compile("/>\w+")
                _publish_name = re.findall(re_words, publish_line[0])
                publish_name = (_publish_name.pop())[2:]  # 发布人昵称
                publish_position = (publish_line[1])[0:-5]  # 发布人职位
                publish_time = (info_publish.find('p').text)[3:]  # 发布时间
                created_at = int(time.time())
                boss_type = self.boss_type
                # SQL 插入语句
                sql = " insert into boss (`job_name`, `job_href`, `money_min`, `money_max`, `address`, `age`, " \
                      "`certificate`,`company_name`, `company_href`, `trade`, `company_round`, `scale`, " \
                      "`publish_href`,`publish_name`, " \
                      "`publish_position`, `publish_time`, `created_at`, `boss_type`) values " \
                      "('%s', '%s', '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                      " '%s', '%s','%d', '%d')" % \
                      (job_name, job_href, money_min, money_max, address, age, certificate, company_name, company_href,
                       trade, company_round, scale, publish_href, publish_name, publish_position, publish_time,
                       created_at, boss_type)
                self.cursor.execute(sql)
                self.db.commit()
                print("正在存入第%d条 --《%s》-- %s" % (i, company_name, money))
                i += 1
            # 续一秒
            time.sleep(1)

start = time.time()
# php
# php = Boss(r'https://www.zhipin.com/c101210100-p100103/', 1, 10)
# php.spider()

# web前端
# web = Boss(r'https://www.zhipin.com/c101210100-p100901/', 2, 10)
# web.spider()

# java
# java = Boss(r'https://www.zhipin.com/c101210100-p100101/', 3, 10)
# java.spider()

# python
py = Boss(r'https://www.zhipin.com/c101210100-p100109/', 4, 10)
py.spider()

end = time.time()
s = end - start
print("总共花费%.2f秒" % s)
