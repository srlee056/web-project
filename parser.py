from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
context = ssl._create_unverified_context()
'''
urllib.error.URLError: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1076)> 
위와같은 오류가 생겨서 ssl import 함 (구글 검색으로 해결법 찾음)
'''


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
    for i in range(1,3):
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
            eventDate = event.find('li',{'class':'contents_descript'}).find('span',{'class':'descript_body'}).text.strip()
            print(eventDate)
            if '십오야' in text:
                fifteenList.append({text:link})
            elif 'SOME' in text:
                someList.append({text:link})
                #할인권 쓰는 썸딜은 모바일 전용인듯?
            elif '%' in text:
                saleList.append({text:link})
            elif 'HOT DEAL' in text:
                hotdealList.append({text:link})
    
for e in fifteenList :
    url = e.link

#for e in fifteenList+someList+saleList+hotdealList:
#    print(e)