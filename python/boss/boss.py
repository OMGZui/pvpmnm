from urllib import request
from bs4 import BeautifulSoup

url = r'https://www.zhipin.com/c101210100-p100103/'
with request.urlopen(url) as f:
    html = f.read().decode('utf-8')

soup = BeautifulSoup(html, 'html.parser')

lists = soup.find('div', class_='job-list').find_all('li')
http = r'https://www.zhipin.com/'
boss_list = list()
for item in lists:
    boss_dict = dict()
    # info-primary
    info_primary = item.find('div', class_='job-primary')
    boss_dict['job_name'] = info_primary.find('div', class_='job-title').text
    boss_dict['job_href'] = http + info_primary.find('div', class_='company-text').a.get('href')
    money = info_primary.find('span', class_='red').text
    money = money.split('-', 1)
    boss_dict['money_min'] = int((money[0])[0:-1])
    boss_dict['money_max'] = int((money[1])[0:-1])
    address = info_primary.find_all('p')[1].strings
    print(type(address))
    address = address.split('\<em class=\"vline\"\>\<\/em\>', 1)
    boss_dict['address'] = address
    # info-company

    # info-publis

    boss_list.append(boss_dict)

print(boss_list[0])
