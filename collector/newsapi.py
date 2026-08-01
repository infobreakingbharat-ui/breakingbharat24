import requests
import config


def fetch_latest_news():

    url = "https://newsdata.io/api/1/latest"

    categories = [
        "top",
        "politics",
        "business",
        "technology",
        "crime",
        "sports",
        "entertainment"
    ]

    all_articles = []

    print("=" * 70)
    print("FETCHING LATEST NEWSDATA ARTICLES")
    print("=" * 70)

    for category in categories:

        print(f"\nFetching Category : {category}")

        params = {
            "apikey": config.NEWSDATA_API_KEY,
            "country": "in",
            "language": "en",
            "category": category,
            "size": 10
        }

        try:

            response = requests.get(
                url,
                params=params,
                timeout=30
            )

            if response.status_code != 200:

                print("API Error")
                print(response.text)
                continue

            data = response.json()

            if data.get("status") != "success":

                print(data)
                continue

            results = data.get("results", [])

            print(f"Articles Found : {len(results)}")

            all_articles.extend(results)

        except Exception as e:

            print("Request Failed")
            print(e)

    print("\n")
    print("=" * 70)
    print(f"TOTAL ARTICLES BEFORE DUPLICATE : {len(all_articles)}")
    print("=" * 70)

    ####################################################
    # Remove Duplicate using Link
    ####################################################

    unique_articles = {}

    for article in all_articles:

        link = article.get("link")

        if link:
            unique_articles[link] = article

    articles = list(unique_articles.values())

    print(f"TOTAL UNIQUE ARTICLES : {len(articles)}")

    ####################################################
    # Convert Format
    ####################################################

    news = []

    for item in articles:

        news.append({

            "title": item.get("title", ""),

            "link": item.get("link", ""),

            "source": item.get("source_name", ""),

            "description": item.get("description", ""),

            "image": item.get("image_url", ""),

            "pubDate": item.get("pubDate", "")

        })

    print("=" * 70)
    print(f"LATEST ARTICLES RETURNED : {len(news)}")
    print("=" * 70)

    return news