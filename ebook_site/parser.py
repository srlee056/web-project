from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
context = ssl._create_unverified_context()
'''
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1076)> 
위와같은 오류가 생겨서 ssl import 함 (구글 검색으로 해결법 찾음)
'''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ebook_site.settings")

import django
django.setup()

from parsed_data.models import ebookData

fifteenList = []
someList = []
saleList = []
hotdealList = []

genre = ['romance']#, 'fantasy', 'bl']
ser = '_serial'
# zip 써서 각 장르별로 받아올 예정

# 두 리스트의 조합을 구하는데 더 나은 방법이 있을까?
# from itertools import product


for g in genre:
    for i in range(1,2):
        url = 'https://ridibooks.com/event/'+g+'?type=ago&page='+str(i)
        html = urlopen(url, context=context)
        bsObject = BeautifulSoup(html.read(), "html.parser")
        romanceEventList = bsObject.find_all('li', {'class':'event_list'})

        for event in romanceEventList :
            eventDesc = event.find('h3',{'class':'event_title'}).find('a')
            text = eventDesc.text.strip() # strip() 함수는 공백 제거 목적
            link = eventDesc.get('href')
            if link.startswith('/'):
                link = ''.join(["https://ridibooks.com",link])
            eventDate = event.find('li',{'class':'contents_descript'}).find('span',{'class':'descript_body'})
            #parsing date to datetime https://stackoverflow.com/questions/8636760/parsing-a-datetime-string-into-a-django-datetimefield/24228410
            #print(eventDate)
            if '십오야' in text:
                fifteenList.append({text:link})
            elif 'SOME' in text:
                someList.append({text:link})
                #할인권 쓰는 썸딜은 모바일 전용인듯?
            elif '%' in text:
                saleList.append({text:link})
            elif 'HOT DEAL' in text:
                hotdealList.append({text:link})

#for e in fifteenList :
#    url = e.link

#method that get metadata of books from event page. 
def getBooksMetadata ():
    booklist = []
    url2 = 'https://ridibooks.com/event/18237'
    html2 = urlopen(url2, context=context)
    bsObject2 = BeautifulSoup(html2.read(), "html.parser")

    subgroup = bsObject2.find_all('div', {'id':'subgroup1'})
    for g in subgroup:
        #books = g.find_all('h3', {'class':'meta_title'}).
        books = g.select(
            'h3 > a'
        )
        booklist +=books

    data = {}
    for b in booklist:
        data[b.text.strip()] = ''.join(['https://ridibooks.com',b.get('href')])
    
    return data

if __name__=='__main__':
    dataDict = getBooksMetadata()
    for t, l in dataDict.items():
        ebookData(title = t, link=l).save()
#for e in fifteenList+someList+saleList+hotdealList:
#    print(e)