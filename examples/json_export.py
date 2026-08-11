"""JSON Export — IndianConstitution Library.

Export the full constitution to JSON, CSV, or Markdown.
"""

from indianconstitution import get_constitution

ic = get_constitution()

# ─────────────────────────────────────────────────────────────────────────
# Multi-format export
# ─────────────────────────────────────────────────────────────────────────
ic.export("json", "constitution_export.json")
print("[OK] Exported to constitution_export.json")

ic.export("csv", "constitution_export.csv")
print("[OK] Exported to constitution_export.csv")

ic.export("markdown", "constitution_export.md")
print("[OK] Exported to constitution_export.md")

print(f"\nTotal articles exported: {len(ic)}")
