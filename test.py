import requests
from bs4 import BeautifulSoup
import time
start =time.time()

cities = []

url = 'https://en.wikipedia.org/wiki/List_of_cities_in_Ukraine'
request =requests.get(url)
date = BeautifulSoup(request.text,'lxml')
# date = date.find('table')
date = date.find('tbody')
for city in date.find_all('tr'):
    try:
        city_name = city.find_all('td')[0].text.replace('[a]','').replace('[b]','').replace('[c]','').replace('[d]','')
        cities.append(city_name)
    except:
        pass
    

# cities = [
#     'Odesa','Dnipro','Donetsk','Alchevsk','Almazna'
# ] 

amount_work = 0
for city in cities:
    url = 'https://en.wikipedia.org/wiki/'+city

    request =requests.get(url)

    soup = BeautifulSoup(request.text,'lxml')
    # print(dir(request))
    # print(request.text)
    city_name =  soup.find('span').text 
    try:
        dd = soup.find('div', id='mw-content-text')

        dd2 = dd.find("div", class_="mw-parser-output")

        out = dd2.find("table", class_="infobox ib-settlement vcard")

        out2 = out.find_all("td", class_="infobox-data")
    except:
        pass

    try:
        population = int(out2[9].text.replace(',',''))
        amount_work +=1
    except:  
        population = 'undefined'
    print(f'name:{city_name},population:{population}')
print(f'Скрипт сработал для {amount_work} из {len(cities)} городов')
print(f'Процесс успеха {amount_work/len(cities)*100}%')
print(f'work time {time.time()-start}')