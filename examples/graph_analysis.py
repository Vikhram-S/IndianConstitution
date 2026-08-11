"""Graph Analysis — IndianConstitution Library.

Demonstrates cross-reference graph construction, centrality analysis,
and community detection using NetworkX.

Requires: pip install "indianconstitution[data]"
"""

import networkx as nx

from indianconstitution import get_constitution

ic = get_constitution()

# ─────────────────────────────────────────────────────────────────────────
# 1. Cross-article references
# ─────────────────────────────────────────────────────────────────────────
related = ic.get_related_articles("32")
print("Article 32 references   :", related["references"])
print("Articles referencing 32 :", related["referenced_by"])

# ─────────────────────────────────────────────────────────────────────────
# 2. Get the raw NetworkX graph for custom analysis
# ─────────────────────────────────────────────────────────────────────────
G = ic.get_graph()
print(f"\nGraph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# ─────────────────────────────────────────────────────────────────────────
# 3. Degree centrality — most referenced articles
# ─────────────────────────────────────────────────────────────────────────
centrality = nx.degree_centrality(G)
top_5 = sorted(centrality, key=centrality.get, reverse=True)[:5]
print("\nMost referenced articles (degree centrality):")
for art_num in top_5:
    article = ic.get_article(art_num)
    title = article.title if article else "Unknown"
    print(f"  Art. {art_num}: {title}  (centrality: {centrality[art_num]:.4f})")

# ─────────────────────────────────────────────────────────────────────────
# 4. PageRank centrality
# ─────────────────────────────────────────────────────────────────────────
top_pr = ic.get_central_articles(limit=5)
print("\nMost central articles (PageRank):")
for art_num, score in top_pr:
    article = ic.get_article(art_num)
    title = article.title if article else "Unknown"
    print(f"  Art. {art_num}: {title}  (PageRank: {score:.6f})")
