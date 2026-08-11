"""Search Examples — IndianConstitution Library.

Demonstrates keyword search with the inverted-index engine.
"""

from indianconstitution import get_constitution, search

# ─────────────────────────────────────────────────────────────────────────
# 1. Quick module-level search
# ─────────────────────────────────────────────────────────────────────────
results = search("equality")
print(f"Found {len(results)} articles containing 'equality':")
for r in results:
    print(f"  [{r.number}] {r.title}")

# ─────────────────────────────────────────────────────────────────────────
# 2. Multi-token search (AND logic — all tokens must appear)
# ─────────────────────────────────────────────────────────────────────────
print("\n--- Multi-token search: 'fundamental right' ---")
results = search("fundamental right", limit=5)
for r in results:
    print(f"  [{r.number}] {r.title}")

# ─────────────────────────────────────────────────────────────────────────
# 3. Search via Constitution instance (identical API)
# ─────────────────────────────────────────────────────────────────────────
ic = get_constitution()
print("\n--- Instance search: 'president parliament' ---")
for r in ic.search("president parliament", limit=5):
    print(f"  [{r.number}] {r.title}")
    # Use .text or .content to access the article body:
    print(f"    Preview: {r.text[:120]}…\n")
