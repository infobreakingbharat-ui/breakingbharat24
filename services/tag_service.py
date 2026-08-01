from ai.groq_client import ask_groq


def generate_tags(article):
    prompt = f"""
Generate 5 SEO tags.

Return comma separated only.

Article:

{article}
"""

    tags = ask_groq(prompt)

    return [tag.strip() for tag in tags.split(",")]