from ai.groq_client import ask_groq


def generate_category(article):
    prompt = f"""
You are a news categorization AI.

Choose ONLY ONE category from this list:

Politics
Business
Sports
Technology
Entertainment
World
Health
Education
Crime

Article:

{article}

Return ONLY category name.
"""

    return ask_groq(prompt).strip()