import os
import requests

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

OUTPUT_DIR = "images/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def download_pexels_image(query, filename="featured.jpg"):

    print("=" * 60)
    print("Downloading Image From Pexels")
    print("=" * 60)

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    url = "https://api.pexels.com/v1/search"

    params = {
        "query": query,
        "per_page": 1,
        "orientation": "landscape"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(response.text)
        return None

    data = response.json()

    if not data["photos"]:
        print("No image found")
        return None

    image_url = data["photos"][0]["src"]["large2x"]

    image = requests.get(image_url)

    image_path = os.path.join(OUTPUT_DIR, filename)

    with open(image_path, "wb") as f:
        f.write(image.content)

    print("Saved:", image_path)

    return image_path