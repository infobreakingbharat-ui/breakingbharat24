import requests


def resolve_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            allow_redirects=True,
            timeout=15
        )

        return response.url

    except Exception:
        return url