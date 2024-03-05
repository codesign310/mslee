
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


def get_blog_info(blog_id):
    # 블로그 정보 가져오기
    url = f"https://m.blog.naver.com/{blog_id}?tab=1"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    blog_title = soup.find('a', class_='ell').get_text(strip=True) if soup.find('a', class_='ell') else "블로그명 없음"
    nickname = soup.find('a', class_='text__j6LKZ').get_text(strip=True) if soup.find('a', class_='text__j6LKZ') else "닉네임 없음"
    subject = soup.find('span', class_='subject__m4PT2').get_text(strip=True).rstrip('ㆍ') if soup.find('span', class_='subject__m4PT2') else "관심분야 없음"
    buddy = soup.find('span', class_='buddy__fw6Uo').get_text(strip=True).rstrip('명의 이웃') if soup.find('span', class_='buddy__fw6Uo') else "이웃 없음"
    total_visitors = soup.find('div', class_='count__T3YO8').get_text(strip=True) if soup.find('div', class_='count__T3YO8') else "숫자를 찾을 수 없습니다."

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    total_posts = "전체글 수를 가져올 수 없습니다."  # 기본값 설정
    try:
        # "목록형 보기" 클릭
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "icon_list__E70Pb"))
        ).click()

        # "전체글" 클릭
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#contentslist_block > div.post_block__XQnk9 > div > h3 > button > span"))
        ).click()

        # "전체글" 수 가져오기
        total_posts_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#root > div.apollo_layer_container > div > div > div > ul > li > a > div > em"))
        )
        total_posts = total_posts_element.text if total_posts_element else "전체글 수를 가져올 수 없습니다."
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

    return {
        "title": blog_title,
        "nickname": nickname,
        "subject": subject,
        "buddy": buddy,
        "total_visitors": total_visitors,
        "total_posts": total_posts
    }



def get_recent_posts(blog_id):
    # 최근 게시물 가져오기
    url = f"https://m.blog.naver.com/{blog_id}"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(10)

    try:
        list_view_button = driver.find_element(By.CLASS_NAME, "icon_list__E70Pb")
        list_view_button.click()
        time.sleep(5)
    except Exception as e:
        print(f"Error occurred while clicking list view button: {e}")
        driver.quit()
        return []

    recent_posts = []
    posts = driver.find_elements(By.CSS_SELECTOR, ".postlist__qxOgF .link__A4O1D")
    for post in posts[:5]:
        title = post.find_element(By.CSS_SELECTOR, ".title__Hj5DO .ell2").text
        url = post.get_attribute("href").split('?')[0]
        date = post.find_element(By.CSS_SELECTOR, ".time__SNGFu").text
        likes = post.find_element(By.CSS_SELECTOR, ".like__vTXys").text
        comments = post.find_element(By.CSS_SELECTOR, ".comment__bWHnT").text
        recent_posts.append({"title": title, "url": url, "date": date, "likes": likes, "comments": comments})

    driver.quit()
    return recent_posts



def check_post_exposure(posts):
    # 포스트 노출 여부 확인
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for post in posts:
        search_url = f"https://m.search.naver.com/search.naver?query={quote_plus(post['title'])}"
        driver.get(search_url)
        time.sleep(5)
        try:
            links = driver.find_elements(By.CSS_SELECTOR, ".title_link")
            post['exposure'] = '노출' if any(post['url'] in link.get_attribute("href") for link in links) else '누락'
        except Exception as e:
            post['exposure'] = '확인 실패'
            print(f"Error occurred while checking search results: {e}")

    driver.quit()
    return posts


# 테스트 코드
if __name__ == "__main__":
    # 블로그 ID
    blog_id = "likeyou310"

    # 블로그 정보 가져오기
    blog_info = get_blog_info(blog_id)
    print("블로그 정보:", blog_info)

    # 최근 게시물 가져오기
    recent_posts = get_recent_posts(blog_id)
    print("최근 게시물:", recent_posts)

    # 포스트 노출 여부 확인
    posts_with_exposure = check_post_exposure(recent_posts)
    print("포스트 노출 여부:", posts_with_exposure)
