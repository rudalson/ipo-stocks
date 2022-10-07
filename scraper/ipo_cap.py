import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome(executable_path='./chromedriver')

url = 'http://www.38.co.kr/html/fund/index.htm?o=k&page='

for idx in range(1, 1):
    browser.get(url+ str(idx))

    df = pd.read_html(browser.page_source)[27]

    df.dropna(axis='index', how='all', inplace=True)
    df.dropna(axis='columns', how='all', inplace=True)

    f_name = 'ipo.csv'

    # 같은 파일이 있는지 찾기 위해 import os를 해준다.
    if os.path.exists(f_name):  # 파일이 있다면? 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else: # 파일이 없다면? 헤더포함
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 완료')

browser.quit()