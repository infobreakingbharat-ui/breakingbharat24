from ai.groq_client import ask_groq


def generate_image_prompt(article):

    prompt = f"""
You are an expert AI image prompt engineer.

Generate ONE professional AI image prompt.

Requirements:

- Ultra realistic editorial photography
- Breaking news style
- Photorealistic
- DSLR camera
- High resolution
- Landscape orientation
- 3:2 aspect ratio
- Composition similar to professional newspaper featured images
- Suitable for 1024x680 featured image
- Cinematic lighting
- Highly detailed
- Natural colors
- Sharp focus
- Wide angle
- Modern journalism style
- Professional composition
- Subject centered with enough background
- Leave safe margins for WordPress cropping
- No text
- No logo
- No watermark
- No captions
- No borders
- No collage
- Single image only
- Output should be suitable for saving as WEBP

The image should clearly represent the following news article.

Return ONLY the image prompt.

Article:

{article}
"""

    return ask_groq(prompt)