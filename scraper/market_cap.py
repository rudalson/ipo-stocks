import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome(executable_path='./chromedriver')
# browser.maximize_window() # 창 최대화

# 1. 페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

# 2. 조회 항목 초기화(체크되어 있는 항목 체크 해제)
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): # 체크된 상태라면?
        checkbox.click() # 클릭 (체크 해제)

# 3. 조회 항목 설정 (원하는 항목)
items_to_select = ['영업이익', '자산총계', '매출액']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') # 부모 엘리먼트 찾아가는 법
    label = parent.find_element(By.TAG_NAME, 'label')
    # print(label.text)
    if label.text in items_to_select:
        checkbox.click()

# 4. 적용하기 버튼 누르기
