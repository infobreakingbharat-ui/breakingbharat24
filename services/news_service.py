from database.db import get_connection


def save_news(news_list):

    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    for article in news_list:

        cursor.execute(
            "SELECT id FROM news WHERE url=?",
            (article["link"],)
        )

        exists = cursor.fetchone()

        if exists:
            skipped += 1
            continue

        cursor.execute("""
        INSERT INTO news(
            title,
            url,
            source,
            published_date
        )
        VALUES (?, ?, ?, ?)
        """, (
            article["title"],
            article["link"],
            article["source"],
            article.get("published", article.get("pubDate", ""))
        ))

        inserted += 1

    conn.commit()
    conn.close()

    return inserted, skipped