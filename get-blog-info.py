import requests
from bs4 import BeautifulSoup

result = requests.get("https://emredurukn.github.io/")
src = result.content
soup = BeautifulSoup(src, "lxml")

article_divs = soup.select(".cf.frame .post")

articles = []

for article_div in article_divs:
    articles.append({
        "title": article_div.select(".post-title")[0].text,
        "url": "https://emredurukn.github.io" + article_div.select(".post-title a")[0]["href"],
        "summary": article_div.select(".post-excerpt")[0].text.replace("\n", "")
    })

print(articles)
