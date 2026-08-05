import os
import time
import requests
from urllib.parse import quote

OUTPUT_DIR = "images/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_image(prompt, filename="featured.jpg"):

    print("=" * 60)
    print("Generating AI Image...")
    print("=" * 60)

    url = (
        f"https://image.pollinations.ai/prompt/{quote(prompt)}"
        "?width=1920&height=1080"
    )

    headers = {
        "User-Agent": "BreakingBharatBot/1.0"
    }

    MAX_RETRIES = 3

    for attempt in range(MAX_RETRIES):

        try:

            print(f"Attempt {attempt+1}/{MAX_RETRIES}")

            response = requests.get(
                url,
                headers=headers,
                timeout=180
            )

            print("Status:", response.status_code)

            if response.status_code == 200:

                image_path = os.path.join(OUTPUT_DIR, filename)

                with open(image_path, "wb") as f:
                    f.write(response.content)

                print("Image Saved:", image_path)

                return image_path

            else:

                print(response.text[:500])

        except Exception as e:

            print(e)

        print("Retrying in 20 seconds...")
        time.sleep(20)

    print("Image generation failed.")

    return None