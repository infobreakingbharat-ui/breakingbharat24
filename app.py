import os
import traceback
import markdown
import config
import time

MAX_NEWS_PER_RUN = int(os.getenv("MAX_NEWS_PER_RUN", 8))
REQUEST_DELAY = int(os.getenv("REQUEST_DELAY", 10))
from services.duplicate_service import is_duplicate
from wordpress.publisher import WordPressPublisher
from database.db import create_tables
from collector.newsapi import fetch_latest_news
from services.news_service import save_news

from resolver.url_resolver import resolve_url
from extractor.article_extractor import extract_article
from images.image_prompt import generate_image_prompt
from images.pexels_image import download_pexels_image
from images.image_generator import generate_image
from services.rewrite_service import rewrite_article
from seo.seo_generator import generate_seo
from services.category_service import generate_category
from services.tag_service import generate_tags


print("=" * 70)
print("🚀 BREAKING BHARAT AI AUTOMATION")
print("=" * 70)

print("\nLoading Configuration...\n")

# =====================================================
# STEP 1 - CREATE DATABASE
# =====================================================

create_tables()

# =====================================================
# STEP 2 - FETCH RSS NEWS
# =====================================================

print("=" * 70)
print("STEP 1 : FETCH RSS NEWS")
print("=" * 70)

news = fetch_latest_news()

print(f"\nTotal Articles Found : {len(news)}")

# Process only first N news
news = news[:MAX_NEWS_PER_RUN]

print(f"Processing only {len(news)} articles this run.")

# =====================================================
# STEP 3 - SAVE INTO DATABASE
# =====================================================
print(news[0])
inserted, skipped = save_news(news)

print("\n")
print("=" * 70)
print("DATABASE REPORT")
print("=" * 70)

print(f"New Articles       : {inserted}")
print(f"Duplicate Articles : {skipped}")

# =====================================================
# STEP 4 - AI PROCESSING
# =====================================================

print("\n")
print("=" * 70)
print("PHASE 2 : AI PROCESSING")
print("=" * 70)

# Only first article for testing
for i, article in enumerate(news, start=1):

    print(f"\nProcessing Article {i}")
    print("-" * 70)

    print("\nTitle:")
    print(article["title"])

    print("\nSource:")
    print(article["source"])

    print("\nRSS URL:")
    print(article["link"])

    # =====================================================
    # Resolve Google URL
    # =====================================================

    print("\nResolving URL...")

    original_url = resolve_url(article["link"])

    print("\nOriginal URL:")
    print(original_url)

    # =====================================================
    # Extract Article
    # =====================================================

    print("\nExtracting Article...")

    extracted = extract_article(original_url)

    if not extracted:

        print("Extraction Failed")

        continue

    print("Extraction Successful")

    # =====================================================
    # Rewrite
    # =====================================================

    print("\nRewriting Article using Groq AI...")

    try:

        rewritten = rewrite_article(
            extracted["title"],
            extracted["text"]
        )

        rewritten = markdown.markdown(rewritten)

    except Exception as e:

        print("=" * 60)
        print("REWRITE ERROR")
        print("=" * 60)
        print(e)

        traceback.print_exc()

        continue
    rewritten = markdown.markdown(rewritten)

    print("Rewrite Completed")
    print("=" * 60)
    print("REWRITTEN ARTICLE")
    print("=" * 60)
    print(rewritten[:1000])   # Print first 1000 characters
    print("=" * 60)

    # =====================================================
    # SEO
    # =====================================================

    print("\nGenerating SEO...")

    try:

        seo = generate_seo(rewritten)

    except Exception as e:

        print("=" * 60)
        print("SEO ERROR")
        print("=" * 60)

        print(e)

        traceback.print_exc()

        continue

    print("SEO Completed")
    print("=" * 60)
    print("SEO RESPONSE")
    print("=" * 60)
    print(type(seo))
    print(seo)
    print("=" * 60)
    print("=" * 60)
    print("SEO RESULT")
    print(seo)
    print("=" * 60)
    print("\n========== SEO ==========")
    print(seo)

    if not seo:
        print("SEO generation failed.")
        continue

    if not seo or not seo.get("title"):

        print("SEO FAILED")
        print("Using fallback values")

        seo = {
            "title": extracted["title"],
            "meta": extracted["text"][:150],
            "slug": extracted["title"].lower().replace(" ", "-"),
            "keyword": extracted["title"]
        }

    print("=" * 60)
    print("FINAL SEO")
    print(seo)
    print("=" * 60)
        
    if not seo.get("slug"):

        seo["slug"] = extracted["title"].lower().replace(" ", "-")
    print("=" * 60)
    print("SEO FINAL")
    print(seo)
    print("=" * 60)
        # =====================================================
    # CATEGORY
    # =====================================================

    print("\nGenerating Category...")

    category = generate_category(rewritten)
    print("=" * 60)
    print("CATEGORY")
    print(category)
    print("=" * 60)

    print(category)

    # =====================================================
    # TAGS
    # =====================================================

    print("\nGenerating Tags...")

    try:
        print("\nGenerating Tags...")
        tags = generate_tags(rewritten)

        print("=" * 60)
        print(tags)
        print("=" * 60)

    except Exception as e:
        print("=" * 60)
        print("TAG ERROR")
        print("=" * 60)
        print(e)
        traceback.print_exc()
        raise
    print("=" * 60)
    print("TAGS")
    print(tags)
    print("=" * 60)
    print("\nGenerating Image Prompt...")

    print("\nGenerating Image Prompt...")

    try:
        image_prompt = generate_image_prompt(rewritten)

        print("=" * 60)
        print("IMAGE PROMPT")
        print("=" * 60)
        print(image_prompt)

    except Exception as e:

        print("=" * 60)
        print("IMAGE PROMPT ERROR")
        print("=" * 60)
        print(e)
        traceback.print_exc()

        print("Skipping this article...")
        continue

    print(image_prompt)

    print("\nDownloading image from Pexels...")

    try:

        image_path = download_pexels_image(seo["title"])

        if image_path is None:

            print("Pexels image not found.")

            print("Trying AI image...")

            image_path = generate_image(image_prompt)

    except Exception as e:

        print("=" * 60)
        print("IMAGE ERROR")
        print("=" * 60)

        print(e)

        traceback.print_exc()

        continue

        print("=" * 60)
        print("IMAGE GENERATION ERROR")
        print("=" * 60)

        print(e)

        traceback.print_exc()

        continue
    print("=" * 60)
    print("IMAGE PATH")
    print(image_path)
    print("Exists:", os.path.exists(image_path))
    print("=" * 60)
    print(image_path)
    print(tags)
    print("=" * 60)
    print("STARTING WORDPRESS PUBLISH")
    print("=" * 60)
    print("=" * 60)
    print("CHECKING DUPLICATE")
    print("=" * 60)

    if is_duplicate(seo["title"]):

        print("Duplicate article found in WordPress.")
        print("Skipping publish.")

        continue

    publisher = WordPressPublisher()

    print("Calling publisher.publish()...")

    result = publisher.publish(
        title=seo["title"],
        content=rewritten,
        excerpt=seo["meta"],
        slug=seo["slug"],
        image_path=image_path,
        category=category,
        tags=tags,
        status="publish"
    )

    print("Publisher Returned:")
    print(result)
    # =====================================================
    # FINAL OUTPUT
    # =====================================================

    print("\n")
    print("=" * 70)
    print("FINAL OUTPUT")
    print("=" * 70)

    print("\nSEO TITLE")
    print("-" * 70)
    print(seo["title"])

    print("\nMETA DESCRIPTION")
    print("-" * 70)
    print(seo["meta"])

    print("\nSLUG")
    print("-" * 70)
    print(seo["slug"])

    print("\nFOCUS KEYWORD")
    print("-" * 70)
    print(seo["keyword"])

    print("\nCATEGORY")
    print("-" * 70)
    print(category)

    print("\nTAGS")
    print("-" * 70)
    print(tags)

    print("\nREWRITTEN ARTICLE")
    print("-" * 70)

    print(rewritten)
    print(f"\nWaiting {REQUEST_DELAY} seconds before next article...\n")
    time.sleep(REQUEST_DELAY)

print("\n")
print("=" * 70)
print("SYSTEM READY")
print("=" * 70)