import csv
import requests
from bs4 import BeautifulSoup
import time
import re
import pandas as pd

def check_none(word):
  if word == None:
    return ''
  else:
    return word.text


pattern = '''(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|
富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村|宮古|富良野|別府|佐伯|黒部|小諸|塩尻|玉野|
周南)市|(?:余市|高市|[^市]{2,3}?)郡(?:玉村|大町|.{1,5}?)[町村]|(?:.{1,4}市)?[^町]{1,4}?区|.{1,7}?[市町村])(.+)'''

num =0
page =10

names =[]
phone_numbers =[]
emails =[]
prefectures =[]
municipalities =[]
street_numbers =[]
localities =[]
urls =[]
ssls =[]

while num <50:
  url = 'https://r.gnavi.co.jp/area/jp/continental/rs/?p='+str(page)
  response = requests.get(url)
  bs = BeautifulSoup(response.text, 'html.parser')
  a_tags = bs.find_all('a', class_ = 'style_titleLink__oiHVJ')
  for i in range(0,len(a_tags)):
    if num==50:
      break
    r = requests.get(a_tags[i].get("href"))
    b = BeautifulSoup(r.content, 'html.parser')
    table = b.find('table', class_ = 'basic-table')
    name = check_none(table.find(id="info-name"))
    phone_number = check_none(table.find(class_="number"))
    email = (table.find(string='お店に直接メールする'))
    if email  == None:
      email =''
    else:
      print(email)
      email = email.parent.get("href")[7:]

    region = check_none(table.find(class_="region"))
    locality = check_none(table.find(class_="locality"))

    result = re.match(pattern, region)
    if result: #正規表現パターンにマッチした場合
      prefecture = result.group(1) #都道府県
      municipality = result.group(2)#市区町村
      street_number = result.group(3) #その他

    url = ''
    ssl = ''
    names += [name]
    phone_numbers += [phone_number]
    emails += [email]
    prefectures += [prefecture]
    municipalities += [municipality]
    street_numbers += [street_number]
    localities += [locality]
    urls += [url]
    ssls += [ssl]
    print(num)
    # gurunabi_list.append([name,phone_number,prefecture,municipalities,
    # street_number,locality])
    num+=1
    time.sleep(5)
  page+=1
    # if i==5:
    #   break



data = {
    '店舗名': names,
    '電話番号': phone_numbers,
    'メールアドレス': emails,
    '都道府県':prefectures,
    '市区町村':municipalities,
    '番地':street_numbers,
    '建物名':localities,
    'URL':urls,
    'SSL':ssls,

}
df = pd.DataFrame(data)
df.to_csv("C:/Users/81802/FINAL_ANSWER/Exercise_for_Pool/python/sample.csv",index=False)

print('終了')




#

# else:
#   print('通信失敗')





# with open("C:/Users/81802/Exercise_for_Pool/python/sample.csv", "a",newline="") as f:
#     writer = csv.writer(f)
#     for i in range(0,len(gurunabi_list)):
#       print(gurunabi_list[i])
#       writer.writerow(gurunabi_list[i])
