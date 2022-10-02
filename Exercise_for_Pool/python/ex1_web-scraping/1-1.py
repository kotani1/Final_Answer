import requests
from bs4 import BeautifulSoup
import time
import re
import pandas as pd


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
header = {
    'User-Agent': user_agent
}

pattern = '''(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|
富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村|宮古|富良野|別府|佐伯|黒部|小諸|塩尻|玉野|
周南)市|(?:余市|高市|[^市]{2,3}?)郡(?:玉村|大町|.{1,5}?)[町村]|(?:.{1,4}市)?[^町]{1,4}?区|.{1,7}?[市町村])(.+)'''

num =0
page =10

names =[]
numbers =[]
emails =[]
prefectures =[]
municipalities =[]
street_numbers =[]
localities =[]
urls =[]
ssls =[]

def bunkatu(region):
  result = re.match(pattern, region)
  if result: #正規表現パターンにマッチした場合
      prefecture = result.group(1) #都道府県
      municipality = result.group(2)#市区町村
      street_number = result.group(3) #その他
  for i in range(0,len(street_number)):
    if street_number[i] in ['1','2','3','4','5','6','7','8','9','0']:
      municipality  += street_number[0:i]
      street_number = street_number[i:]
      break
  return [prefecture,municipality,street_number]

while num <50:
  time.sleep(5)
  url = 'https://r.gnavi.co.jp/area/jp/continental/rs/?p='+str(page)
  r = requests.get(url,headers=header)
  b = BeautifulSoup(r.text, 'html.parser')
  a_tags = b.find_all('a', class_ = 'style_titleLink__oiHVJ')
  for i in range(0,len(a_tags)):
    if num==50:
      break
    time.sleep(5)
    r2 = requests.get(a_tags[i].get("href"),headers=header)
    b2 = BeautifulSoup(r2.content, 'html.parser')
    table = b2.find('table', class_ = 'basic-table')
    name = table.find(id="info-name").text
    number = table.find(class_="number").text
    region = table.find(class_="region").text
    adress = bunkatu(region)

    try:
      email = table.find(string='お店に直接メールする').parent.get("href")[7:]
    except:
      email =''

    try:
      locality = table.find(class_="locality").text
    except:
      locality =''



    url = ''
    ssl = ''
    names += [name]
    numbers += [number]
    emails += [email]
    prefectures += [adress[0]]
    municipalities += [adress[1]]
    street_numbers += [adress[2]]
    localities += [locality]
    urls += [url]
    ssls += [ssl]
    num+=1
  page+=1

data = {
    '店舗名': names,
    '電話番号': numbers,
    'メールアドレス': emails,
    '都道府県':prefectures,
    '市区町村':municipalities,
    '番地':street_numbers,
    '建物名':localities,
    'URL':urls,
    'SSL':ssls,
}
df = pd.DataFrame(data)
df.to_csv("C:/FINAL_ANSWER/Exercise_for_Pool/python/ex1_web-scraping/1-1.csv",index=False,encoding="cp932", errors='ignore'
)

print('終了')
