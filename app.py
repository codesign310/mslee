from flask import Flask, render_template, request
from naver_keyword import get_results as get_keyword_results, search_blog, search_news
from post_detail import get_crawled_post_data  # post_detail.py에서 함수 가져오기
from blog import get_blog_info, get_recent_posts, check_post_exposure



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
        post_url = request.form['post_url']  # 사용자가 입력한 포스트 URL 받아오기
        post_data = get_crawled_post_data(post_url)  # post_detail.py의 함수 호출하여 데이터 가져오기
        
        #텍스트 길이 검수
        post_textlength = post_data["post_textlength"]
        text_length_result = '🔵 적절한 글자수입니다.' if post_textlength >= 1000 else '🔴 1,000자 이상 작성을 추천해요.'
        
        
        return render_template('contents.html', post_data=post_data, text_length_result=text_length_result) 
    else:
        return render_template('contents.html', post_data=None)





@app.route('/blog', methods=['GET', 'POST'])
def blog_view():
    if request.method == 'POST':
        # 폼 데이터에서 'blog_id'를 가져옵니다.
        blog_id = request.form.get('blog_id')
        
        # blog.py의 함수를 호출하여 결과를 가져옵니다.
        blog_info = get_blog_info(blog_id)
        recent_posts = get_recent_posts(blog_id)
        posts_with_exposure = check_post_exposure(recent_posts)
        
        # 결과 데이터와 함께 blog.html을 렌더링합니다.
        return render_template('blog.html', blog_info=blog_info, recent_posts=recent_posts, posts_with_exposure=posts_with_exposure)
    else:
        # GET 요청의 경우, 단순히 폼만 포함된 blog.html을 렌더링합니다.
        return render_template('blog.html')





if __name__ == '__main__':
    app.run(debug=True)


#if __name__ == '__main__':
#   app.run(debug=False, port=5000)
