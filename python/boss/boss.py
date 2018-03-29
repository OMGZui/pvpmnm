from urllib import request
from bs4 import BeautifulSoup
import re
import pymysql
import time

start = time.time()
# 打开数据库连接
db = pymysql.connect("localhost", "root", "root", "pvpmnm", use_unicode=True, charset="utf8")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

for j in range(10):
    url = r'https://www.zhipin.com/c101210100-p100103/?page=%d' % (j + 1)
    # 抓取
    with request.urlopen(url) as f:
        html = f.read().decode('utf-8')

    soup = BeautifulSoup(html, 'html.parser')

    lists = soup.find('div', class_='job-list').find_all('li')
    http = r'https://www.zhipin.com'

    # 解析
    i = 30*j+1
    for item in lists:
        # info-primary
        info_primary = item.find('div', class_='job-primary')
        job_name = info_primary.find('div', class_='job-title').text  # 岗位名字
        job_href = http + info_primary.find('a').get('href')  # 详情链接
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
        company_href = http + info_company.find('a').get('href')  # 公司链接
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

        # SQL 插入语句
        sql = " insert into boss (`job_name`, `job_href`, `money_min`, `money_max`, `address`, `age`, `certificate`, " \
              "`company_name`, `company_href`, `trade`, `company_round`, `scale`, `publish_href`, `publish_name`, " \
              "`publish_position`, `publish_time`, `created_at`) values " \
              "('%s', '%s', '%d', '%d', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')" % \
              (job_name, job_href, money_min, money_max, address, age, certificate, company_name, company_href, trade,
               company_round, scale, publish_href, publish_name, publish_position, publish_time, created_at)
        cursor.execute(sql)
        db.commit()
        print("正在存入第%d条 --《%s》-- %s" % (i, company_name, money))
        i += 1
    time.sleep(1)
# 关闭数据库连接
db.close()
end = time.time()

s = end - start
print("总共花费%.2f秒" % s)

"""
{'job_name': '中级PHP开发', 'job_href': 'https://www.zhipin.com/job_detail/1418606307.html', 'money_min': 8,
 'money_max': 13, 'address': '杭州 西湖区 黄龙', 'age': '1年以内', 'certificate': '本科', 'company_name': '浙江校联',
 'company_href': 'https://www.zhipin.com/gongsi/766208.html', 'trade': '移动互联网',
 'company_round': '不需要融资', 'scale': '20-99', 'publish_href': 'https://i\.jpg', 'publish_name': '陈秀梅',
 'publish_position': '人事经理', 'publish_time': '03月27日'}
 """
