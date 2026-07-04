from sqlalchemy import Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import TSVECTOR

from yarn_plugin.recommendations.infrastructure.repository.full_text_search import (
    or_tsquery,
    search_vector_matches,
)


def compiled(expression: object) -> tuple[str, dict[str, object]]:
    compiled_expr = expression.compile(dialect=postgresql.dialect())  # type: ignore[attr-defined]
    return str(compiled_expr), dict(compiled_expr.params)


def test_combines_words_with_or_not_and() -> None:
    sql, params = compiled(or_tsquery("yarn for beginners"))

    assert "||" in sql
    assert "&&" not in sql
    assert sql.count("plainto_tsquery(") == 3
    assert set(params.values()) == {"simple", "yarn", "for", "beginners"}


def test_uses_simple_config_not_english() -> None:
    _, params = compiled(or_tsquery("wool"))

    assert "simple" in params.values()
    assert "english" not in params.values()


def test_drops_short_words_to_avoid_spurious_matches() -> None:
    # Reproduces the exact false-positive found via manual MCP testing: the single-letter "a"
    # in "llana per a principiants" spuriously matched unrelated content containing "a" as a word.
    _, params = compiled(or_tsquery("llana per a principiants"))

    assert "a" not in params.values()
    assert "llana" in params.values()
    assert "per" in params.values()  # 3 letters — kept; this is an approximation, not a real stopword list
    assert "principiants" in params.values()


def test_falls_back_to_full_words_when_all_are_short() -> None:
    _, params = compiled(or_tsquery("a i o"))

    assert "a" in params.values()
    assert "i" in params.values()
    assert "o" in params.values()


def test_search_vector_matches_builds_containment_operator() -> None:
    search_vector = Column("search_vector", TSVECTOR)
    sql, _ = compiled(search_vector_matches(search_vector, "wool"))

    assert "@@" in sql
