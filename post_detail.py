import requests
from bs4 import BeautifulSoup



def get_crawled_post_data(post_url):
    url = post_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 카테고리 
    post_category_element = soup.find(class_='blog_category')
    post_categroy = post_category_element.get_text() if post_category_element else "못찾음"
    
    # 포스트 제목
    post_title_element = soup.find(class_='se-title-text')
    post_title = post_title_element.get_text() if post_title_element else "못찾음"

    # 닉네임 
    post_nick_element = soup.find(class_='blog_author')
    post_nick = post_nick_element.get_text() if post_nick_element else "못찾음"

    # 작성일/시간 
    post_date_element = soup.find(class_='blog_date')
    post_date = post_date_element.get_text() if post_date_element else "못찾음"
    
    # 텍스트 수
    post_textlength_element = soup.find(class_='se-main-container').find_all(class_='se-text-paragraph')
    post_textlength = sum(len(text.get_text(strip=True)) for text in post_textlength_element)

    # 이미지 수
    post_imgcount_element = soup.find(class_='se-main-container').find_all(class_='se-module-image')
    post_imgcount = len(post_imgcount_element)

    # 링크 수
    post_link_element = soup.find(class_='se-main-container').find_all('a', class_='se-link')
    post_linkcount = len(post_link_element)

    # 태그
    post_tag_element = soup.select('.post_tag .ell')
    post_tag = [tag.text for tag in post_tag_element]

    # 좋아요 수 
    post_like_element = soup.find('em', class_='u_cnt _count')
    post_like = post_like_element.get_text() if post_like_element else "못찾음"

    # 댓글 수
    post_comment_element = soup.find('div', class_='btn_r').find('em')
    post_comment = post_comment_element.get_text() if post_comment_element else "못찾음"
    
    # 동영상 수
    post_video_element = soup.find(class_='se-main-container').find_all(class_='se-module-video')
    post_videocount = len(post_video_element)


    post_detail = {
        "post_title": post_title,
        "post_category": post_categroy,
        "post_nick": post_nick,
        "post_date": post_date,
        "post_like": post_like,
        "post_comment": post_comment,
        "post_textlength": post_textlength,
        "post_imgcount": post_imgcount,
        "post_linkcount": post_linkcount,
        "post_tag": post_tag,
        "post_videocount": post_videocount
    }

    return post_detail


# 테스트 코드
if __name__ == "__main__":
    # 테스트할 포스트 URL
    test_post_url = "https://m.blog.naver.com/likeyou310/222862013005"

    # get_crawled_post_data 함수 호출
    post_data = get_crawled_post_data(test_post_url)

    # 결과 출력
    print("포스트 제목:", post_data["post_title"])
    print("포스트 카테고리:", post_data["post_category"])
    print("포스트 닉네임:", post_data["post_nick"])
    print("포스트 작성일:", post_data["post_date"])
    print("포스트 좋아요 수:", post_data["post_like"])
    print("포스트 댓글 수:", post_data["post_comment"])
    print("포스트 텍스트 길이:", post_data["post_textlength"])
    print("포스트 이미지 수:", post_data["post_imgcount"])
    print("포스트 링크 수:", post_data["post_linkcount"])
    print("포스트 태그:", post_data["post_tag"])
    print("포스트 동영상 수:", post_data["post_videocount"])
