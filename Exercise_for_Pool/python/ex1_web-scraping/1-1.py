import requests
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

headers = {
'User-Agent': 'ootatarou1@gmail.com'
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

while num <50:
  url = 'https://r.gnavi.co.jp/area/jp/continental/rs/?p='+str(page)
  response = requests.get(url,headers=headers)
  bs = BeautifulSoup(response.text, 'html.parser')
  a_tags = bs.find_all('a', class_ = 'style_titleLink__oiHVJ')
  for i in range(0,len(a_tags)):
    if num==50:
      break
    r = requests.get(a_tags[i].get("href"),headers=headers)
    b = BeautifulSoup(r.content, 'html.parser')
    table = b.find('table', class_ = 'basic-table')
    name = table.find(id="info-name").text
    number = table.find(class_="number").text
    try:
      email = table.find(string='お店に直接メールする').parent.get("href")[7:]
    except:
      email =''
    try:
      locality = table.find(class_="locality").text
    except:
      locality =''
    region = table.find(class_="region").text
    result = re.match(pattern, region)
    if result: #正規表現パターンにマッチした場合
      prefecture = result.group(1) #都道府県
      municipality = result.group(2)#市区町村
      street_number = result.group(3) #その他

    url = ''
    ssl = ''
    names += [name]
    numbers += [number]
    emails += [email]
    prefectures += [prefecture]
    municipalities += [municipality]
    street_numbers += [street_number]
    localities += [locality]
    urls += [url]
    ssls += [ssl]
    num+=1
    time.sleep(5)
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
df.to_csv("C:/FINAL_ANSWER/Exercise_for_Pool/python/ex1_web-scraping/1-1.csv",index=False)

print('終了')
