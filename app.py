from flask import Flask, render_template, request
from naver_keyword import get_results as get_keyword_results, search_blog, search_news
from post_detail import get_crawled_post_data  # post_detail.py에서 함수 가져오기


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def naver_keyword():
    keyword_results, total_blog_results, blog_results, total_news_results, news_results = None, None, None, None, None

    if request.method == 'POST':
        keyword_input = request.form['naver_keyword'].replace(" ", "") 
        keyword_results = get_keyword_results(keyword_input)
        total_blog_results, blog_results = search_blog(keyword_input)
        total_news_results, news_results = search_news(keyword_input)

    return render_template('index.html', keyword_results=keyword_results, total_blog_results=total_blog_results, blog_results=blog_results, total_news_results=total_news_results, news_results=news_results)



@app.route('/contents', methods=['GET', 'POST'])
def contents():
    if request.method == 'POST':
        post_url = request.form.get('post_url')  # 사용자가 입력한 포스트 URL 받아오기

        # URL 변환을 수행
        if 'm.blog.naver.com' in post_url:
            # 이미 모바일 버전 URL인 경우
            converted_post_url = post_url
        elif 'blog.naver.com' in post_url:
            # 데스크톱 버전 URL인 경우 모바일 버전으로 변환
            converted_post_url = post_url.replace('blog.naver.com', 'm.blog.naver.com')
        else:
            # 다른 사이트의 URL이거나 올바르지 않은 URL인 경우
            return render_template('error.html', message='URL을 다시 확인해주세요.')

        post_data = get_crawled_post_data(converted_post_url)  # post_detail.py의 함수 호출하여 데이터 가져오기

        if post_data:
            # 가져온 데이터가 있는 경우
            return render_template('contents.html', post_data=post_data)
        else:
            # 가져온 데이터가 없는 경우
            return render_template('error.html', message='결과를 찾을 수 없습니다.')
    else:
        return render_template('contents.html', post_data=None)



#if __name__ == '__main__':
#    app.run(debug=True)


if __name__ == '__main__':
   app.run(debug=False, port=5000)
