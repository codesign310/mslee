import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote_plus
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome 드라이버를 설정
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')

# Chrome 브라우저를 headless 모드로 실행
driver = webdriver.Chrome(service=service, options=options)

# 웹페이지에 접속
driver.get("https://m.zum.com/")

# 버튼을 클릭하여 데이터 로드
button = driver.find_element(By.CSS_SELECTOR, "#app > div > header > div.issue-keyword > div.wrap-keyword > div > button")
button.click()

# 데이터가 로드될 때까지 대기 (10초로 설정)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#app > div > header > div.issue-keyword > div.keyword-list > div"))
)

# BeautifulSoup을 사용하여 페이지 소스 가져오기
soup = BeautifulSoup(driver.page_source, "html.parser")

# 데이터 추출 및 출력
items = soup.select("div[data-v-141ba2c1] li a")
for item in items:
    # 텍스트 추출
    text = item.find("span", class_="rank").find_next_sibling(text=True).strip()

    # 링크 추출 및 Naver 뉴스 검색 링크 생성
    query = quote_plus(text)
    naver_news_link = f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={query}"
    print("텍스트:", text)
    print("Naver 뉴스 검색 링크:", naver_news_link)
    print()

# 드라이버 종료
driver.quit()
