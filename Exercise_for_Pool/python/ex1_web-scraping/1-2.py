import re
import time
import pandas as pd
from selenium import webdriver
driver = webdriver.Chrome(executable_path="C:/Users/81802/Downloads/chromedriver_win32/chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument('--user-agent=ootatarou1@gmail.com')

num =0
names =[]
numbers =[]
emails =[]
prefectures =[]
municipalities =[]
street_numbers =[]
localities =[]
urls =[]
ssls =[]

pattern = '''(...??[都道府県])((?:旭川|伊達|石狩|盛岡|奥州|田村|南相馬|那須塩原|東村山|武蔵村山|羽村|十日町|上越|
富山|野々市|大町|蒲郡|四日市|姫路|大和郡山|廿日市|下松|岩国|田川|大村|宮古|富良野|別府|佐伯|黒部|小諸|塩尻|玉野|
周南)市|(?:余市|高市|[^市]{2,3}?)郡(?:玉村|大町|.{1,5}?)[町村]|(?:.{1,4}市)?[^町]{1,4}?区|.{1,7}?[市町村])(.+)'''


driver.get("https://r.gnavi.co.jp/area/jp/japanese/rs/")

while num <50:
  a_tags = driver.find_elements_by_class_name('style_titleLink__oiHVJ')
  for i in range(0,len(a_tags)):
    if num ==50:
      break
    driver.execute_script("window.open('"+ a_tags[i].get_attribute("href")+"');")
    driver.switch_to.window(driver.window_handles[1])
    name = driver.find_element_by_id("info-name").text
    number = driver.find_element_by_class_name("number").text
    email = driver.find_elements_by_link_text('お店に直接メールする')
    if email:
      email = email[0].get_attribute("href")[7:]
    else:
      email =''
    region = driver.find_element_by_class_name("region").text
    result = re.match(pattern, region)
    if result: #正規表現パターンにマッチした場合
      prefecture = result.group(1) #都道府県
      municipality = result.group(2)#市区町村
      street_number = result.group(3) #その他

    locality = driver.find_elements_by_class_name("locality")
    if locality:
      locality = locality[0].text
    else:
      locality = ''

    url = driver.find_elements_by_class_name("sv-of")
    if url:
      url = url[0].get_attribute("href")
      if url[4:5] == 's':
        ssl = 'True'
    else:
      url = ''
      ssl = 'False'
    names += [name]
    numbers += [number]
    emails += [email]
    prefectures += [prefecture]
    municipalities += [municipality]
    street_numbers += [street_number]
    localities += [locality]
    urls += [url]
    ssls += [ssl]

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    num+=1
    time.sleep(5)
  driver.find_element_by_class_name('style_nextIcon__M_Me_').click()
  time.sleep(1)
driver.close()
driver.quit()
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
df.to_csv("C:/FINAL_ANSWER/Exercise_for_Pool/python/1-2.csv")

print('終了')
