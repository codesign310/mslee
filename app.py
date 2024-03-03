from flask import Flask, render_template, request
from naver_keyword import get_results as get_keyword_results, search_blog, search_news

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

if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == '__main__':
#    app.run(debug=False, port=5000)