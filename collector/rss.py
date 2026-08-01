import feedparser

RSS_FEEDS = [
    {
        "name": "Google News India",
        "url": "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    },
    {
        "name": "The Hindu",
        "url": "https://www.thehindu.com/news/feeder/default.rss"
    },
    {
        "name": "India Today",
        "url": "https://www.indiatoday.in/rss/home"
    }
]


def fetch_news():

    articles = []

    for feed in RSS_FEEDS:

        print(f"\nReading : {feed['name']}")

        data = feedparser.parse(feed["url"])

        print(f"Articles Found : {len(data.entries)}")

        for entry in data.entries:

            articles.append({
                "source": feed["name"],
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", "")
            })

    return articles