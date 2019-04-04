import requests
from bs4 import BeautifulSoup

result = requests.get("https://www.imdb.com/title/tt2306299/")

src = result.content
soup = BeautifulSoup(src, "lxml")

nodes = soup.select("#top-rated-episodes-rhs .episode-container")

print(nodes[1].select(".title-row a")[0].text)

top_rated_episodes = []

for node in nodes:
    top_rated_episodes.append(
        {
            "title" : node.select(".title-row a")[0].text,
            "description" : node.select("p:nth-child(2)")[0].text,
            "star_rating" : node.select(".ipl-rating-star > span.ipl-rating-star__rating")[0].text
        }
    )

print(top_rated_episodes)