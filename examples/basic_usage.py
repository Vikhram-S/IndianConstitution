"""Basic Usage — IndianConstitution Library.

Demonstrates core article retrieval, search, and data exploration.
"""

from indianconstitution import get_article, get_constitution, search

# ─────────────────────────────────────────────────────────────────────────
# 1. Retrieve a single article by number
# ─────────────────────────────────────────────────────────────────────────
article = get_article("21A")
if article:
    print(f"Article {article.number}: {article.title}")
    print(f"Content preview: {article.content[:200]}…\n")

# ─────────────────────────────────────────────────────────────────────────
# 2. Sub-millisecond keyword search via inverted index
# ─────────────────────────────────────────────────────────────────────────
results = search("right to equality", limit=5)
print(f"Found {len(results)} articles for 'right to equality':")
for r in results:
    print(f"  [{r.number}] {r.title}")

# ─────────────────────────────────────────────────────────────────────────
# 3. Access the full Constitution object
# ─────────────────────────────────────────────────────────────────────────
ic = get_constitution()
print(f"\nPreamble (first 200 chars): {ic.preamble[:200]}…")
print(f"Total articles loaded: {len(ic)}")

# ─────────────────────────────────────────────────────────────────────────
# 4. Iterate over all articles
# ─────────────────────────────────────────────────────────────────────────
fundamental_rights = [a for a in ic.articles if a.part == 3]
print(f"\nPart III (Fundamental Rights) articles: {len(fundamental_rights)}")
for a in fundamental_rights[:5]:
    print(f"  Art. {a.number}: {a.title}")
