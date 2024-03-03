from flask import Flask, render_template, request, jsonify
from naver_keyword import get_results as get_keyword_results, search_blog, search_news



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def naver_keyword():
    if request.method == 'POST':
        keyword_input = request.form['naver_keyword']
        keyword_results = get_keyword_results(keyword_input)
        total_blog_results, blog_results = search_blog(keyword_input)
        total_news_results, news_results = search_news(keyword_input)

        if keyword_results and blog_results and news_results:
            return render_template('index.html', keyword_results=keyword_results, total_blog_results=total_blog_results, blog_results=blog_results, total_news_results=total_news_results, news_results=news_results)
        else:
            return render_template('index.html', keyword_results=None, total_blog_results=None, blog_results=None, total_news_results=None, news_results=None)
    else:
        return render_template('index.html', keyword_results=None, total_blog_results=None, blog_results=None, total_news_results=None, news_results=None)



if __name__ == '__main__':
    app.run(debug=True)
