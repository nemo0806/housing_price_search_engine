import lxml.html
import requests
import re
import csv


pagenum=1
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}

cityqueryURL = 'https://bj.lianjia.com/ershoufang'
cityquerypage = requests.get(cityqueryURL, headers=headers)
cityquery_tree = lxml.html.fromstring(cityquerypage.content)
cityhtmllist = cityquery_tree.xpath("//div[@class='link-list']/div[5]/dd/a/@href")           
citylist = ['https://{}.lianjia.com/ershoufang/pg'.format(i[8:10]) for i in cityhtmllist]
# del citylist[0]
for city in citylist:
    try:
        for pagenum in range(1,100):
            queryURL = city + str(pagenum)
            querypage = requests.get(queryURL, headers=headers)
            query_tree = lxml.html.fromstring(querypage.content)
            house_name = query_tree.xpath("//div[@class='info clear']/div[@class='title']/a/text()")
            house_link = query_tree.xpath("//div[@class='info clear']/div[@class='title']/a/@href")
            house_xiaoqu = query_tree.xpath("//div[@class='houseInfo']/a/text()")
            house_info = query_tree.xpath("//div[@class='houseInfo']/text()")
            house_posinfo = query_tree.xpath("//div[@class='positionInfo']/text()")
            house_folinfo = query_tree.xpath("//div[@class='followInfo']/text()")
            house_price = query_tree.xpath("//div[@class='totalPrice']/span/text()")
            house_unitprice = query_tree.xpath("//div[@class='unitPrice']/@data-price")

            house_info_split = [k.split(' | ') for k in house_info]
            house_posinfo_strip = [l.strip(' -') for l in house_posinfo]
            house_folinfo_split = [m.split(' / ') for m in house_folinfo]


            for i in range(len(house_name)-1):
                # house_info_dict = {}
                # for j in range(4):
                #     if house_info[i+j].find('平米') != -1:
                #         house_info_dict['area'] = house_info[i+j]
                #     elif house_info[i+j].find('电梯') != -1:
                #         house_info_dict['elevator'] = house_info[i+j]
                #     elif house_info[i+j].find('精装')
                # house_info_split[i] = [l.strip() for l in house_info_split[i]]
                for detail in house_info_split[i]:
                    if detail.find('平米') != -1:
                        house_area = detail
                        house_info_split[i].remove(detail)
                        break
                        
                with open('{}_spiderbypage.csv'.format(city[8:10]), 'a', encoding='utf-8', newline='') as f:
                    csvwriter = csv.writer(f, dialect='excel')
                    csvwriter.writerow([
                        house_name[i],
                        house_link[i],
                        house_xiaoqu[i].strip(),
                        house_area,
                        ' '.join(house_info_split[i]),
                        house_posinfo_strip[i],
                        house_folinfo_split[i][0],
                        house_folinfo_split[i][1],
                        house_folinfo_split[i][2],
                        house_price[i],
                        house_unitprice[i]
                    ])
    except Exception:
        print(city, "exception occurred")
        continue