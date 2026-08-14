from ai.groq_client import ask_groq


def generate_seo(article):

    prompt = f"""
Generate SEO for this article.

IMPORTANT LANGUAGE INSTRUCTION:
- Generate TITLE in Hindi.
- Generate META description in Hindi.
- Generate KEYWORD in Hindi.
- Generate SLUG using English lowercase words separated by hyphens.
- The main news content is Hindi, so understand the article and generate SEO accordingly.
- Use natural, professional Hindi suitable for a Hindi news website.
- Do not write the TITLE or META in English.
- Do not use unnecessary English words.
- Keep person names, company names, brand names and place names in their commonly used form.

SEO requirements:
- TITLE should be a compelling Hindi news headline.
- META should be a natural Hindi SEO meta description.
- SLUG should be short, lowercase English words separated by hyphens.
- KEYWORD should be the primary Hindi search keyword.

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