import os
import requests
from urllib.parse import quote

OUTPUT_DIR = "images/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_image(prompt, filename="featured.jpg"):

    print("=" * 60)
    print("Generating AI Image...")
    print("=" * 60)

    url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"

    print("Image URL:")
    print(url)

    headers = {
        "User-Agent": "BreakingBharatBot/1.0"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=180
        )

        print("Status Code:", response.status_code)

        content_type = response.headers.get("Content-Type")
        print("Content-Type:", content_type)

        if response.status_code != 200:
            print("Image Generation Failed")
            print(response.text[:1000])
            return None

        if not content_type or "image" not in content_type.lower():
            print("Response is not an image")
            print(response.text[:1000])
            return None

        image_path = os.path.join(OUTPUT_DIR, filename)

        with open(image_path, "wb") as f:
            f.write(response.content)

        print("Image Saved Successfully")
        print("Saved At:", image_path)

        return image_path

    except Exception as e:
        print("=" * 60)
        print("IMAGE GENERATION ERROR")
        print("=" * 60)
        print(e)
        return None

if __name__ == "__main__":

    prompt = """
    Ultra realistic editorial news image,
    breaking news,
    dramatic lighting,
    newspaper featured image,
    no text,
    no watermark,
    4k,
    photorealistic
    """

    path = generate_image(prompt)

    print("Returned Path:", path)