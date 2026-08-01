import requests
import config
from rapidfuzz import fuzz


def is_duplicate(title):

    response = requests.get(
        f"{config.WP_URL}/wp-json/wp/v2/posts",
        params={
            "per_page": 100
        }
    )

    if response.status_code != 200:
        return False

    posts = response.json()

    for post in posts:

        score = fuzz.ratio(
            title.lower(),
            post["title"]["rendered"].lower()
        )

        if score > 85:
            print("Duplicate Score:", score)
            print(post["title"]["rendered"])
            return True

    return False