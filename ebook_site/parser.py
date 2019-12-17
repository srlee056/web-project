from urllib.request import urlopen
from bs4 import BeautifulSoup

import enum
import ssl
context = ssl._create_unverified_context()
'''
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1076)> 
위와같은 오류가 생겨서 ssl import 함 (구글 검색으로 해결법 찾음)
'''
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "ebook_site.settings")

import django
django.setup()
from parsed_data.models import EbookData, EventData, EventLog

class Page(enum.IntEnum):
    PRE = 0
    PAST = 5

class EventType(enum.IntEnum):
    FT = 0 #fifthteen
    SOME = 1
    SALE = 2 #percent sale
    HD = 3 #hotdeal

PP = ['']
for i in range(1, Page.PAST+1):
    PP.append('?type=ago&page='+str(i))

fifteenList = []
someList = []
saleList = []
hotdealList = []

genre = ['romance']#, 'fantasy', 'bl']
ser = '_serial'


# 현재, 지난 이벤트들의 주소를 위한 리스트.

# zip 써서 각 장르별로 받아올 예정

# 두 리스트의 조합을 구하는데 더 나은 방법이 있을까?
# from itertools import product

def getEventsMetadata():
    data = {}
    for g in genre:
        for i in range(1, Page.PAST+1):
            url = 'https://ridibooks.com/event/'+g+PP[i]
            html = urlopen(url, context=context)
            bsObject = BeautifulSoup(html.read(), "html.parser")
            eventList = bsObject.select(
                '#page_event_list > ul.event_list_wrapper > li'
            )

            for event in eventList :
                eventDesc = event.find('h3',{'class':'event_title'}).find('a')
                text = eventDesc.text.strip() # strip() 함수는 공백 제거 목적
                link = eventDesc.get('href')
                if link.startswith('/'):
                    link = ''.join(["https://ridibooks.com",link])
                date = event.find('li',{'class':'contents_descript'}).find('span',{'class':'descript_body'}).text.strip()
                #parsing date to datetime https://stackoverflow.com/questions/8636760/parsing-a-datetime-string-into-a-django-datetimefield/24228410
                
                if '십오야' in text:
                    t = EventType.FT
                elif 'SOME' in text:
                    t = EventType.SOME
                elif '%' in text:
                    t = EventType.SALE
                elif 'HOT DEAL' in text:
                    t = EventType.HD
                else:
                    continue
                data[text] = (link, date, g, t)
    return data

#method that get metadata of books from event page. 
def getBooksMetadata (url):
    #url = 'https://ridibooks.com/event/18237'
    html = urlopen(url, context=context)
    bsObject = BeautifulSoup(html.read(), "html.parser")

    booklist = bsObject.select(
        '#subgroup1 > div > div.book_metadata_wrapper > h3 > a'
    )
    #print(booklist)

    data = {}
    for b in booklist:
        data[b.text.strip()] = ''.join(['https://ridibooks.com',b.get('href')])
    
    return data

if __name__=='__main__':
    eventDataDict = getEventsMetadata()
    for t, (l, d, g, ty) in eventDataDict.items():
        eD = EventData(title = t, link = l, date = d, genre=g, eType = ty)
        eD.save()

        ebookDataDict = getBooksMetadata(l)
        for t, l in ebookDataDict.items():
            bD = EbookData(title = t, link=l)
            bD.save()

            EventLog(event=eD, ebook=bD).save()



    '''
    dictionary 에 튜플로 value를 넣는것보다
    dict list를 만들고
    data[name] = ''
    data[link] = 'https:// ..'
    이렇게 하는게 나으려나...

    '''