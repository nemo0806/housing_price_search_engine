from lxml import html
import requests
import re
import multiprocessing as mp
import csv

quote_page = 'https://bj.lianjia.com/ershoufang'
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
}

# page = requests.get(quote_page, headers = headers)

# with open("1.html", 'r', encoding='utf-8') as f:
#     html1 = f.read()

# root_tree = html.fromstring(html1)

# house_link = root_tree.xpath("//ul[@class='sellListContent']/li/a/@href")
# house_code = root_tree.xpath("//ul[@class='sellListContent']/li/a/@data-housecode")
# print(house_link)
# print(len(house_link))
# print(house_code)
enumhousecode = r"10110[23]\d{5}"

def spiderit(URL):
    pass






def multiquery(processnum, totalnum):
    batch_size = int(4000000/totalnum)
    start = 101100000000 + batch_size*(processnum-1)
    end = start + batch_size
    for query in range(start,end):
        queryURL = 'https://bj.lianjia.com/ershoufang/rs' + str(query)
        querypage = requests.get(queryURL, headers=headers)
        query_tree = html.fromstring(querypage.content)
        if query_tree.xpath("//div[@class='m-noresult']"):
            print('process[{}]'.format(processnum), query, 'continue')
            continue
        else:
            house_name = query_tree.xpath("//div[@class='info clear']/div[@class='title']/a/text()")
            house_link = query_tree.xpath("//div[@class='info clear']/div[@class='title']/a/@href")
            house_xiaoqu = query_tree.xpath("//div[@class='houseInfo']/a/text()")
            house_info = query_tree.xpath("//div[@class='houseInfo']/text()")
            house_posinfo = query_tree.xpath("//div[@class='positionInfo']/text()")
            house_folinfo = query_tree.xpath("//div[@class='followInfo']/text()")
            house_price = query_tree.xpath("//div[@class='totalPrice']/span/text()")
            house_unitprice = query_tree.xpath("//div[@class='unitPrice']/@data-price")

            # for i in range(len(house_name)-1):
            i = 0
            house_detail_info = [house_info[i+j] for j in range(4)]
            for detail in house_detail_info:
                if detail.find('平米') != -1:
                    house_area = detail
                    house_detail_info.remove(detail)
                    break
                    
            with open('spiderbypage.csv', 'a', encoding='utf-8', newline='') as f:
                csvwriter = csv.writer(f, dialect='excel')
                csvwriter.writerow([
                    house_name[i],
                    house_link[i],
                    house_xiaoqu[i],
                    # house_info[5*i],
                    # house_info[5*i+1],
                    # house_info[5*i+2],
                    # house_info[5*i+3],
                    # house_info[5*i+4],
                    house_area,
                    ' '.join(house_detail_info),
                    house_posinfo[2*i],
                    house_posinfo[2*i+1],
                    house_folinfo[2*i],
                    house_folinfo[2*i+1],
                    house_price[i],
                    house_unitprice[i]
                ])

                print('==get=it==', query)




class LockedProcess(mp.Process):
    def __init__(self, lock, totalnum, processnum):
        mp.Process.__init__(self)
        self.lock = lock
        self.totalnum = totalnum
        self.processnum = processnum
 
    def run(self):
        batch_size = 1000000//self.totalnum
        start = 101101000000 + batch_size*(self.processnum-1)
        end = start + batch_size
        headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
        }
        for query in range(start,end):
            queryURL = 'https://bj.lianjia.com/ershoufang/rs' + str(query)
            querypage = requests.get(queryURL, headers=headers)
            query_tree = html.fromstring(querypage.content)
            if query_tree.xpath("//div[@class='m-noresult']"):
                # self.lock.acquire()
                print('process[{}]'.format(self.processnum), query, 'continue')
                # self.lock.release()
                continue
            else:
                house_name = query_tree.xpath("//div[@class='info clear']/div[@class='title']/a[1]")
                house_link = query_tree.xpath("//div[@class='info clear']/div[@class='title']/a[1]/@href")
                # self.lock.acquire()
                print(query, house_name, house_link)
                # self.lock.release()

    





if __name__ == '__main__':
    totalnum = 80
    mp.freeze_support()
    # pool = mp.Pool(processes = totalnum)
    # for processnum in range(1, totalnum):
    #     pool.map_async(multiquery,[processnum, totalnum])
    # pool.close()
    # pool.join()
    
    
    
    processlist=[mp.Process(target=multiquery, args=(processnum,totalnum,)) for processnum in range(1,totalnum)]
    # for processnumber in range(1,totalnum):
    #     p = mp.Process(target=multiquery, args=(processnumber,totalnum,))
    #     p.daemon = True
    #     p.start()

    for process in processlist:
        process.daemon=True
        process.start()
    
    for process in processlist:
        process.join()
    
           
    
 





