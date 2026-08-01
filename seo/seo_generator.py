from ai.groq_client import ask_groq


def generate_seo(article):

    prompt = f"""
Generate SEO for this article.

Return exactly:

TITLE:
META:
SLUG:
KEYWORD:

Article:

{article}
"""

    response = ask_groq(prompt)

    seo = {
        "title": "",
        "meta": "",
        "slug": "",
        "keyword": ""
    }

    for line in response.splitlines():

        if line.startswith("TITLE:"):
            seo["title"] = line.replace("TITLE:", "").strip()

        elif line.startswith("META:"):
            seo["meta"] = line.replace("META:", "").strip()

        elif line.startswith("SLUG:"):
            seo["slug"] = line.replace("SLUG:", "").strip()

        elif line.startswith("KEYWORD:"):
            seo["keyword"] = line.replace("KEYWORD:", "").strip()

    return seo