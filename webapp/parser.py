import requests
from bs4 import BeautifulSoup
from datetime import datetime
from webapp.db import db
from webapp.news.models import News


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except requests.RequestException:
        return False


def get_python_news(url):
    print('collecting news')
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    all_news = soup.find('ul', class_='list-recent-posts menu')
    for news in all_news.find_all('li'):
        title = news.find('h3').text
        url = news.find('a')['href']
        date = news.find('time')['datetime']
        date = datetime.strptime(date, '%Y-%m-%d')
        text = BeautifulSoup(get_html(url), 'html.parser').find('div', class_='date-posts')
        text = text.decode_contents()
        save_news(title, url, date, text)
    # return rows

def save_news(title, url, date, text):
    news_exist = News.query.filter(News.url == url).count()
    if not news_exist:
        new_news = News(
            title=title,
            url=url,
            date=date,
            text=text,
        )
        db.session.add(new_news)
        db.session.commit()


if __name__ == '__main__':
    get_python_news('http://python.org/blog')
