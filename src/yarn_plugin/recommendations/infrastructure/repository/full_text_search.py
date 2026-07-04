from typing import Any

from sqlalchemy import ColumnElement, func

MIN_SEARCH_WORD_LENGTH = 3


def or_tsquery(query_text: str) -> ColumnElement[Any]:
    """Build a tsquery matching ANY word in query_text (OR), using the language-agnostic
    'simple' config — so partial phrase matches (e.g. "yarn for beginners" when only
    "beginners" appears in the data) still return results, and non-English queries aren't
    silently dropped by English-specific stemming.

    'simple' has no stopword list for any language, so short filler words ("a", "i", "el", "de")
    would otherwise become search terms and cause spurious one-letter/two-letter matches. Words
    shorter than MIN_SEARCH_WORD_LENGTH are dropped before building the query — an approximation
    of stopword filtering, not a real per-language stopword list. Falls back to the full word list
    if every word in the query is that short, so the search never becomes a no-op.
    """
    words = [word for word in query_text.split() if len(word) >= MIN_SEARCH_WORD_LENGTH] or query_text.split()
    combined: ColumnElement[Any] = func.plainto_tsquery("simple", words[0])
    for word in words[1:]:
        combined = combined.op("||")(func.plainto_tsquery("simple", word))
    return combined


def search_vector_matches(search_vector: ColumnElement[Any], query_text: str) -> ColumnElement[bool]:
    return search_vector.op("@@")(or_tsquery(query_text))
