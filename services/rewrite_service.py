from ai.groq_client import ask_groq


def rewrite_article(title, article):

    prompt = f"""
You are an experienced Indian news journalist.

Rewrite the following article.

Rules:

- 100% original
- Human tone
- Professional journalism style
- Do NOT copy sentences
- Keep all facts unchanged
- Use headings
- Use short paragraphs
- Around 600-900 words

TITLE

{title}

ARTICLE

{article}
"""

    return ask_groq(prompt)