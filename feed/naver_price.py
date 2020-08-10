from bs4 import BeautifulSoup
import requests
import time
import random
import pickle
import sys, os, django, re
from datetime import datetime
import pickle
from django.db.models import Q
from django.utils import timezone

sys.path.append(os.path.abspath("/home/bai/belluz")
os.environ['DJANGO_SETTINGS_MODULE'] = 'belluz.settings'
django.setup()


def get_crp_cds():
    url = 'http://34.85.70.128/api/v1/news/getCorp/original/'
    res = requests.get(url)
    if res.status_code == 200:
        res = res.json()
    else:
        res = None
    crp_cds = [crp_dict['crp_cd'] for crp_dict in res]
    crp_nms = [crp_dict['crp_nm'] for crp_dict in res]
    return crp_cds, crp_nms


def check_if_under_priced(crp_cd, crp_nm):
    web_link = 'https://finance.naver.com/item/main.nhn?code=' + crp_cd
    result = requests.get(web_link)
    bs_obj = BeautifulSoup(result.content, "html.parser")

    no_today = bs_obj.find("p", {"class": "no_today"})
    blind = no_today.find("span", {"class": "blind"})
    now_price = int(blind.text.replace(",", ""))

    invest_info = bs_obj.find_all("table", {"summary": "투자의견 정보"})[0]
    ems = invest_info.find_all("em")

    buy_signal = float(ems[0].text)
    expected_price = ems[1].text.replace(",", "")

    pbr = bs_obj.find("em", {"id": '_pbr'})
    pbr = float(pbr.text)

    if expected_price == 'N/A':
        return False, None, None, None, None
    else:
        expected_price = int(expected_price)

    print("기업명:", crp_nm)
    print("현재주가:", now_price)
    print("매수의견:", buy_signal)
    print("목표주가:", expected_price)
    print("PBR:", pbr)

    suggested = False

    if pbr < 1.3 and 3.0< buy_signal and expected_price > now_price:
        suggested = True
        print("추천:", "BUY")
    else:
        print("추천:", "DONT BUY")

    print("\n")

    return suggested, buy_signal, expected_price, now_price, pbr


if __name__ == "__main__":

     crp_cds, crp_nms = get_crp_cds()
    
     the_list = list()
     for index, crp_cd in enumerate(crp_cds):
         try:
             result, buy_signal, expected_price, now_price, pbr = check_if_under_priced(crp_cd, crp_nms[index])
             if result:
                 the_list.append([crp_cd, crp_nms[index], buy_signal, expected_price, now_price, pbr])
             rand_int = round(random.uniform(7,13),4)
             time.sleep(rand_int)
         except Exception as e:
             pass
    
	 # dump용 DB 용
     with open("buy_list.pkl", 'wb') as f:
         pickle.dump(the_list, f, protocol=pickle.HIGHEST_PROTOCOL)
	 for crp_group in the_list:
		
   # with open("buy_list.pkl", 'rb') as f:
   #     the_list = pickle.load(f)
   # 
   # new_list = list()
   # for ind, crp_list in enumerate(the_list):
   #     # print(str(ind))
   #     # print("기업명:", crp_list[1])
   #     # print("매수의견:", crp_list[2])
   #     # print("목표주가:", crp_list[3])
   #     # print("현재주가:", crp_list[4])
   #     # print("PBR:", crp_list[5])
   #     
   #     expected_price = crp_list[3]
   #     current_price = crp_list[4]
   #     percentage = (expected_price - current_price)/ expected_price
   #     new_list.append([percentage, crp_list[0],crp_list[1],crp_list[2],crp_list[3],crp_list[4],crp_list[5]])
   # 
   # new_list.sort(key=lambda x:x[0], reverse=True)

    for ind, crp_list in enumerate(new_list[:20]):
        print(str(ind))
        print("percentage:", crp_list[0])
        print("기업명:", crp_list[2])
        print("매수의견:", crp_list[3])
        print("목표주가:", crp_list[4])
        print("현재주가:", crp_list[5])
        print("PBR:", crp_list[6])

