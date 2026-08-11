"""RAG Pipeline Integration — IndianConstitution Library.

Demonstrates building a constitutional context block for LLM prompting.
This is the pattern documented in the README.
"""

from indianconstitution import get_constitution

ic = get_constitution()


def build_rag_context(query: str, top_k: int = 3) -> str:
    """Build a constitutional context block for LLM prompting.

    Uses the inverted-index search to find relevant articles,
    then formats them for injection into an LLM prompt.
    """
    results = ic.search(query, limit=top_k)
    context_blocks = []
    for article in results:
        context_blocks.append(
            f"**Article {article.number} -- {article.title}**\n"
            f"{article.text}\n"  # .text is an alias for .content
        )
    return "\n---\n".join(context_blocks)


# ─────────────────────────────────────────────────────────────────────────
# Example: Generate RAG context for a legal query
# ─────────────────────────────────────────────────────────────────────────
query = "equality"
context = build_rag_context(query)

print(f"RAG Context for: '{query}'\n")
print("=" * 60)
print(context if context else "(No keyword match)")
print("=" * 60)

# ─────────────────────────────────────────────────────────────────────────
# Example: Full prompt template
# ─────────────────────────────────────────────────────────────────────────
prompt_template = f"""You are a constitutional law expert. Answer the question
using ONLY the constitutional provisions below. Cite article numbers.

CONSTITUTIONAL CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""

print(f"\n{'-' * 60}")
print("Full LLM Prompt:")
print(f"{'-' * 60}")
print(prompt_template)
