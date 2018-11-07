require 'open-uri'
require 'nokogiri'
require 'json'

def url_valid?(url)
	url = URI.parse(url) rescue false
	url.kind_of?(URI::HTTP) || url.kind_of?(URI::HTTPS)
end

def normalize_uri(uri)
    return uri if uri.is_a? URI

    uri = uri.to_s
    uri, *tail = uri.rpartition "#" if uri["#"]

    URI(URI.encode(uri) << Array(tail).join)
end

user_agent = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3080.30 Safari/537.36", "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36", "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"]
top_rated_episodes = []
url = "https://www.imdb.com/title/tt2306299/"   # Vikings imdb page

if url_valid?(url)
    dc = open(url, 'User-Agent' => user_agent[rand(4)])
else
    begin
        dc = open(normalize_uri(url), 'User-Agent' => user_agent[rand(4)])
    rescue => error
        puts error
        dc = open(url, { ssl_verify_mode: 0 })
    end
end

pc = Nokogiri::HTML(dc.read, nil, "UTF-8")

pc.css("#top-rated-episodes-rhs .episode-container").each do |episode|
    top_rated_episodes.push({
        :title => episode.css(".title-row > a").first.inner_text,
        :description => episode.css("p:nth-child(2)").inner_text,
        :star_rating => episode.css(".ipl-rating-star > span.ipl-rating-star__rating").first.inner_text
    })
end

File.open("top-rated-episodes.json","w") do |f|
    f.write(JSON.pretty_generate(top_rated_episodes))
end