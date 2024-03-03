import os
import sys
import urllib.request
import json
import time
import random
import requests
import hashlib
import hmac
import base64

class Signature:
    @staticmethod
    def generate(timestamp, method, uri, secret_key):
        message = "{}.{}.{}".format(timestamp, method, uri)
        hash_obj = hmac.new(bytes(secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)
        signature = base64.b64encode(hash_obj.digest()).decode('utf-8')
        return signature

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = Signature.generate(timestamp, method, uri, secret_key)
    
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 
            'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': signature}

def get_results(hintKeywords, max_results=1):
    BASE_URL = 'https://api.naver.com'
    API_KEY = '010000000011b01165a53e36f295a6bc80d8eedf0bb8dacb00ea14ca7f470dcde91c5b11a2'
    SECRET_KEY = 'AQAAAAAg2SCxaCcCuFwARYmSFftiLEidnHqxIUl5FluJxErnaw=='
    CUSTOMER_ID = '1406414'
    uri = '/keywordstool'
    method = 'GET'
    params = {'hintKeywords': hintKeywords, 'showDetail': '1'}
    r = requests.get(BASE_URL + uri, params=params, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    keyword_list = r.json()['keywordList']
    return keyword_list[:max_results]

def search_blog(query, display=5, start=1, sort='sim'):
    BASE_URL = 'https://openapi.naver.com/v1/search/blog.json'
    headers = {
        'X-Naver-Client-Id': 'c9IfTncbqHQJkt8ThQ2j',
        'X-Naver-Client-Secret': '8X7fyIxVBZ'
    }
    params = {
        'query': query,
        'display': display,
        'start': start,
        'sort': sort
    }
    
    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        results = response.json()
        total_results = results['total']
        blog_items = results['items']
        return total_results, blog_items
    else:
        print("Error:", response.status_code)
        return None, None

def search_news(query, display=5, start=1, sort='sim'):
    BASE_URL = 'https://openapi.naver.com/v1/search/news.json'
    headers = {
        'X-Naver-Client-Id': 'c9IfTncbqHQJkt8ThQ2j',
        'X-Naver-Client-Secret': '8X7fyIxVBZ'
    }
    params = {
        'query': query,
        'display': display,
        'start': start,
        'sort': sort
    }
    
    response = requests.get(BASE_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        results = response.json()
        total_results = results['total']
        news_items = results['items']
        return total_results, news_items
    else:
        print("Error:", response.status_code)
        return None, None


