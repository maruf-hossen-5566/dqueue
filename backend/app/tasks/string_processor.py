from collections import Counter

from app.tasks.registry import task


@task("string_process")
async def string_process(payload: str):
    if not payload:
        raise ValueError("Payload is missing")

    if not payload.strip():
        raise ValueError("Data not in payload")

    long_text = Counter(payload.replace(".", "").lower().split())

    total_chars = len(payload)
    top_words = long_text.most_common(3)
    word_count = len(payload.split())

    return {
        "top_words": top_words,
        "character_count": total_chars,
        "word_count": word_count,
    }
