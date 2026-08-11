"""Pandas Integration — IndianConstitution Library.

Demonstrates DataFrame creation and analysis with pandas.

Requires: pip install "indianconstitution[data]"
"""

import pandas as pd

from indianconstitution import get_constitution

ic = get_constitution()

# ─────────────────────────────────────────────────────────────────────────
# 1. Direct DataFrame from articles (using Pydantic v2 model_dump)
# ─────────────────────────────────────────────────────────────────────────
df = pd.DataFrame([a.model_dump() for a in ic.data.articles])
print("DataFrame shape:", df.shape)
print("\nFirst 10 articles:")
print(df[["number", "title", "part"]].head(10).to_string(index=False))

# ─────────────────────────────────────────────────────────────────────────
# 2. Convenience method (equivalent, but shorter)
# ─────────────────────────────────────────────────────────────────────────
df2 = ic.to_dataframe()
print(f"\nConvenience method — same shape: {df2.shape}")

# ─────────────────────────────────────────────────────────────────────────
# 3. Basic analytics
# ─────────────────────────────────────────────────────────────────────────
print("\nArticles per Part:")
part_counts = df["part"].value_counts().sort_index()
for part, count in part_counts.items():
    if part is not None:
        print(f"  Part {int(part):>3d}: {count} articles")

# Word-count distribution
df["word_count"] = df["content"].apply(lambda x: len(str(x).split()))
print(f"\nAverage words per article: {df['word_count'].mean():.0f}")
print(f"Longest article: Art. {df.loc[df['word_count'].idxmax(), 'number']} "
      f"({df['word_count'].max()} words)")
