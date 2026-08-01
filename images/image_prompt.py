from ai.groq_client import ask_groq


def generate_image_prompt(article):

    prompt = f"""
You are an expert prompt engineer.

Create a professional image generation prompt for an AI image model.

Rules:

- Ultra realistic
- Editorial photography
- Breaking news style
- Cinematic lighting
- Highly detailed
- 8K
- 16:9 composition
- No text
- No watermark
- No logo
- Newspaper featured image
- Photorealistic
- High quality

Return ONLY the image prompt.

Article:

{article}
"""

    return ask_groq(prompt)