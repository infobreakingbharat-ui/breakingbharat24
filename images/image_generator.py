import os
import requests
from urllib.parse import quote

OUTPUT_DIR = "images/output"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_image(prompt, filename="featured.jpg"):

    print("Generating AI Image...")

    url = f"https://image.pollinations.ai/prompt/{quote(prompt)}"

    response = requests.get(url, timeout=120)

    if response.status_code != 200:
        print("Image Generation Failed")
        return None

    image_path = os.path.join(OUTPUT_DIR, filename)

    with open(image_path, "wb") as f:
        f.write(response.content)

    print("Image Saved Successfully")

    return image_path


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

    print(path)