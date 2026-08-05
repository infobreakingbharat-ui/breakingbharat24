import os
import json
import mimetypes
import requests
from requests.auth import HTTPBasicAuth
import config


class WordPressPublisher:

    def __init__(self):
        self.base_url = config.WP_URL.rstrip("/")

        self.media_url = f"{self.base_url}/wp-json/wp/v2/media"
        self.post_url = f"{self.base_url}/wp-json/wp/v2/posts"
        self.tag_url = f"{self.base_url}/wp-json/wp/v2/tags"
        self.category_url = f"{self.base_url}/wp-json/wp/v2/categories"

        self.auth = HTTPBasicAuth(
            config.WP_USERNAME,
            config.WP_APP_PASSWORD
        )

    ####################################################
    # Upload Featured Image
    ####################################################
    def upload_image(self, image_path):

        # No image provided
        if image_path is None:
            print("No image provided. Skipping upload.")
            return None

        # Image path does not exist
        if not os.path.exists(image_path):
            print("Image not found.")
            return None

        filename = os.path.basename(image_path)
        mime = mimetypes.guess_type(image_path)[0] or "image/jpeg"

        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": mime
        }

        with open(image_path, "rb") as img:

            response = requests.post(
                self.media_url,
                headers=headers,
                data=img.read(),
                auth=self.auth
            )

        if response.status_code not in [200, 201]:
            print(response.text)
            return None

        media = response.json()

        print("Image Uploaded")

        return media["id"]

    ####################################################
    # Get or Create Category
    ####################################################
    def get_category(self, category_name):

        response = requests.get(
            self.category_url,
            params={"search": category_name},
            auth=self.auth
        )

        if response.status_code == 200:

            data = response.json()

            for item in data:
                if item["name"].lower() == category_name.lower():
                    return item["id"]

        payload = {
            "name": category_name
        }

        response = requests.post(
            self.category_url,
            json=payload,
            auth=self.auth
        )

        if response.status_code in [200, 201]:
            return response.json()["id"]

        return None

    ####################################################
    # Get or Create Tag
    ####################################################
    def get_tag(self, tag):

        response = requests.get(
            self.tag_url,
            params={"search": tag},
            auth=self.auth
        )

        if response.status_code == 200:

            data = response.json()

            for item in data:
                if item["name"].lower() == tag.lower():
                    return item["id"]

        payload = {
            "name": tag
        }

        response = requests.post(
            self.tag_url,
            json=payload,
            auth=self.auth
        )

        if response.status_code in [200, 201]:
            return response.json()["id"]

        return None

    ####################################################
    # Publish Post
    ####################################################
    def publish(

            self,
            title,
            content,
            excerpt,
            slug,
            image_path,
            category,
            tags,
            status="publish"

    ):

        media_id = None

        if image_path:
            media_id = self.upload_image(image_path)
        else:
            print("Publishing without featured image.")

        category_id = self.get_category(category)

        tag_ids = []

        for tag in tags:
            tag_id = self.get_tag(tag)

            if tag_id:
                tag_ids.append(tag_id)
        payload = {
            "title": title,
            "content": content,
            "excerpt": excerpt,
            "slug": slug,
            "status": status,
            "categories": [category_id] if category_id else [],
            "tags": tag_ids
        }

        # Add featured image only if uploaded successfully
        if media_id:
            payload["featured_media"] = media_id

        response = requests.post(

            self.post_url,

            json=payload,

            auth=self.auth

        )

        if response.status_code not in [200, 201]:
            print("Image Upload Failed")
            print(response.status_code)
            print(response.text)
            return None

        post = response.json()

        print("Published Successfully")

        print(post["link"])

        return post