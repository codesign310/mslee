import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def get_zum_links():
    # 웹페이지에 GET 요청을 보내고 응답을 받아옴
    response = requests.get("https://m.zum.com/")

    # 응답 내용을 BeautifulSoup을 사용하여 파싱
    soup = BeautifulSoup(response.text, "html.parser")

    # 데이터 추출 및 출력
    items = soup.select("div[data-v-141ba2c1] li a")
    
    results = []
    for item in items:
        # 텍스트 추출
        text = item.find("span", class_="rank").find_next_sibling(text=True).strip()

        # 링크 추출 및 Naver 뉴스 검색 링크 생성
        query = quote_plus(text)
        naver_news_link = f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={query}"
        
        results.append({"text": text, "naver_news_link": naver_news_link})

    return results

if __name__ == "__main__":
    zum_links = get_zum_links()
    for link in zum_links:
        print("텍스트:", link["text"])
        print("Naver 뉴스 검색 링크:", link["naver_news_link"])
        print()
