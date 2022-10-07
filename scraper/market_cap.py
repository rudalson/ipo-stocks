import os
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
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

for idx in range(1, 40): # 1 이상 40 미만 페이지 반복
    # 사전 작업 : 페이지 이동
    browser.get(url + str(idx)) # http://url...&page=2

    # 5. 데이터 추출
    # 그냥 추출하니깐 len(df)는 3이 나왔는데 실제 2번째것이 주식 관련 내용이었다.
    # 따라서 바로 [1]을 붙이면 df는 필요한 부분의 테이블을 1차로 가져 온다.
    df = pd.read_html(browser.page_source)[1]

    # >>> df.head(10)
    #      N       종목명       현재가     전일비     등락률  ...      영업이익  토론실  Unnamed: 10  Unnamed: 11  Unnamed: 12
    # 0  NaN       NaN       NaN     NaN     NaN  ...       NaN  NaN          NaN          NaN          NaN
    # 1  1.0      삼성전자   56200.0   100.0  -0.18%  ...  516339.0  NaN          NaN          NaN          NaN
    # 2  2.0  LG에너지솔루션  482500.0  4500.0  +0.94%  ...    7685.0  NaN          NaN          NaN          NaN
    # 3  3.0    SK하이닉스   91200.0  1300.0  +1.45%  ...  124103.0  NaN          NaN          NaN          NaN
    # 4  4.0  삼성바이오로직스  811000.0  1000.0  -0.12%  ...    5373.0  NaN          NaN          NaN          NaN
    # 5  5.0     삼성전자우   51100.0   500.0  +0.99%  ...       NaN  NaN          NaN          NaN          NaN
    # 6  NaN       NaN       NaN     NaN     NaN  ...       NaN  NaN          NaN          NaN          NaN
    # 7  NaN       NaN       NaN     NaN     NaN  ...       NaN  NaN          NaN          NaN          NaN
    # 8  NaN       NaN       NaN     NaN     NaN  ...       NaN  NaN          NaN          NaN          NaN
    # 9  6.0      LG화학  589000.0  6000.0  +1.03%  ...   50255.0  NaN          NaN          NaN          NaN


    # 네이버 주식화면을 보면 divider를 테이블 항목으롣 구현해놓았다. divider부분은 NaN으로 처리되어 있다.
    # Nan 즉 결측치가 있는 항목을 삭제하는데 Nan이 all 인 경우를 지워라. any인 경우는 하나라도 있으면 이라는 조건.
    # inplace=True는 변경한 항목을 df에 반영하는 것이고 이게 없으면 변경한 내용을 return 한다.
    df.dropna(axis='index', how='all', inplace=True)
    # >>> df.head(10)
    #        N       종목명       현재가     전일비     등락률     액면가        매출액       자산총계      영업이익  토론실  Unnamed: 10  Unnamed: 11  Unnamed: 12
    # 1    1.0      삼성전자   56200.0   100.0  -0.18%   100.0  2796048.0  4266212.0  516339.0  NaN          NaN          NaN          NaN
    # 2    2.0  LG에너지솔루션  482500.0  4500.0  +0.94%   500.0   178519.0   237641.0    7685.0  NaN          NaN          NaN          NaN
    # 3    3.0    SK하이닉스   91200.0  1300.0  +1.45%  5000.0   429978.0   963865.0  124103.0  NaN          NaN          NaN          NaN
    # 4    4.0  삼성바이오로직스  811000.0  1000.0  -0.12%  2500.0    15680.0    79700.0    5373.0  NaN          NaN          NaN          NaN
    # 5    5.0     삼성전자우   51100.0   500.0  +0.99%   100.0        NaN        NaN       NaN  NaN          NaN          NaN          NaN
    # 9    6.0      LG화학  589000.0  6000.0  +1.03%  5000.0   426547.0   511353.0   50255.0  NaN          NaN          NaN          NaN
    # 10   7.0     삼성SDI  591000.0  6000.0  +1.03%  5000.0   135532.0   258332.0   10676.0  NaN          NaN          NaN          NaN
    # 11   8.0       현대차  175500.0  2500.0  -1.40%  5000.0  1176106.0  2339464.0   66789.0  NaN          NaN          NaN          NaN
    # 12   9.0        기아   71000.0   500.0  -0.70%  5000.0   698624.0   668500.0   50657.0  NaN          NaN          NaN          NaN
    # 13  10.0     NAVER  160000.0  7000.0  -4.19%   100.0    68176.0   336910.0   13255.0  NaN          NaN          NaN          NaN

    df.dropna(axis='columns', how='all', inplace=True)
    # >>> df.head(10)
    #        N       종목명       현재가     전일비     등락률     액면가        매출액       자산총계      영업이익
    # 1    1.0      삼성전자   56200.0   100.0  -0.18%   100.0  2796048.0  4266212.0  516339.0
    # 2    2.0  LG에너지솔루션  482500.0  4500.0  +0.94%   500.0   178519.0   237641.0    7685.0
    # 3    3.0    SK하이닉스   91200.0  1300.0  +1.45%  5000.0   429978.0   963865.0  124103.0
    # 4    4.0  삼성바이오로직스  811000.0  1000.0  -0.12%  2500.0    15680.0    79700.0    5373.0
    # 5    5.0     삼성전자우   51100.0   500.0   +0.99%   100.0        NaN        NaN       NaN
    # 9    6.0      LG화학  589000.0  6000.0  +1.03%  5000.0   426547.0   511353.0   50255.0
    # 10   7.0     삼성SDI  591000.0  6000.0  +1.03%  5000.0   135532.0   258332.0   10676.0
    # 11   8.0       현대차  175500.0  2500.0  -1.40%  5000.0  1176106.0  2339464.0   66789.0
    # 12   9.0        기아   71000.0   500.0  -0.70%  5000.0   698624.0   668500.0   50657.0
    # 13  10.0     NAVER  160000.0  7000.0  -4.19%   100.0    68176.0   336910.0   13255.0

    if len(df) == 0: # 더 이상 가져올 데이터가 없으면?
        break

    # 6. 파일 저장 
    f_name = 'sise.csv'

    # 같은 파일이 있는지 찾기 위해 import os를 해준다.
    if os.path.exists(f_name):  # 파일이 있다면? 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else: # 파일이 없다면? 헤더포함
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 완료')

browser.quit()   # 브라우저 종료