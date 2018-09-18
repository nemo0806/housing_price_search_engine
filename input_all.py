# coding: utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "housing_price.settings")

import django
django.setup()


def main():
    VE = 0  # ValueError Counter
    VK = 0  # KeyError Counter

    city_dict = {'bj': 'Beijing',
                 'gz': 'Guangzhou',
                 'cd': 'Chengdu',
                 'cq': 'Chongqing',
                 'cs': 'Changsha',
                 'dg': 'Dongguan',
                 'dl': 'Dalian',
                 'fs': 'Foshan',
                 'hf': 'Hefei',
                 'hz': 'Hangzhou',
                 'jn': 'Jinan',
                 'nj': 'Nanjing',
                 'qd': 'Qingdao',
                 'sy': 'Shenyang',
                 'sz': 'Shenzhen',
                 'tj': 'Tianjin',
                 'wh': 'Wuhan',
                 'wx': 'Wuxi',
                 'xa': "Xi'an",
                 'xm': 'Xiamen',
                 'yt': 'Yantai',
                 'zh': 'Zhuhai',
                 'zs': 'Zhongshan',
                 'zz': 'Zhengzhou'
                 }

    from search.models import House
    with open(r"E:\PycharmProjects\housing_price\housing_all.txt", "r", encoding= 'gbk') as f:
        s = f.readlines()
        List = []
        for ele in s:
#            print (ele)
            parts = ele.split(',')

#            print (parts)

            try:
                parts[3] = float(parts[3])
                parts[10] = float(parts[10][:-1])
                List.append(House(name=parts[0] + ' ' + parts[1] + ' ' + parts[4] + parts[5] + parts[6] + parts[7] + parts[8], city= city_dict[parts[1][8:10]], location=parts[2], area=parts[3], price=parts[10]))
            except ValueError:
                VE += 1
                continue
            except KeyError:
                VK += 1
                continue
            except:
                continue

#        print(List)
        House.objects.bulk_create(List)

    print('%i ValueError occurred\n' % VE)
    print('%i KeyError occurred\n' % VK)

if __name__ == "__main__":
    main()
    print ("Done!")