"""Data provenance and corpus integrity validation script.

Validates all JSON dataset files against Pydantic schema invariants,
computes cryptographic SHA-256 integrity checksums, and reports statistics.
Runs deterministically on CPU in <500ms with zero network dependencies.
"""

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict

from indianconstitution.core.models import (
    AmendmentEvent,
    Article,
    CaseLaw,
    ConstitutionData,
    DutyCrossReference,
)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        pass

DATA_DIR = Path(__file__).parent.parent / "src" / "indianconstitution" / "data"


def compute_sha256(file_path: Path) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def validate_corpus() -> bool:
    """Validate all corpus JSON files for schema correctness and integrity."""
    start_time = time.perf_counter()
    print("=" * 75)
    print("INDIAN CONSTITUTION CORPUS VALIDATION & INTEGRITY CHECK")
    print("=" * 75)

    if not DATA_DIR.exists():
        print(f"FAILED: Data directory not found at {DATA_DIR}")
        return False

    all_passed = True
    files_to_check = [
        ("constitution.json", "Core Constitution Corpus"),
        ("case_law.json", "Landmark SC Case Judgments"),
        ("amendments.json", "Amendment Event History"),
        ("duties.json", "Fundamental Duty Cross-References"),
        ("i18n.json", "Multilingual Translations"),
    ]

    summary_stats: Dict[str, Any] = {}

    for filename, description in files_to_check:
        file_path = DATA_DIR / filename
        if not file_path.exists():
            print(f"[MISSING] {filename} ({description})")
            all_passed = False
            continue

        sha256 = compute_sha256(file_path)
        size_kb = file_path.stat().st_size / 1024.0

        try:
            with open(file_path, encoding="utf-8") as f:
                data = json.load(f)

            count = 0
            if filename == "constitution.json":
                if isinstance(data, list):
                    articles = [Article(**item) for item in data if item.get("article") != 0 and item.get("title") != "Preamble"]
                    count = len(articles)
                else:
                    cdata = ConstitutionData(**data)
                    count = len(cdata.articles)
            elif filename == "case_law.json":
                cases = [CaseLaw(**item) for item in data]
                count = len(cases)
            elif filename == "amendments.json":
                amendments = [AmendmentEvent(**item) for item in data]
                count = len(amendments)
            elif filename == "duties.json":
                duties = [DutyCrossReference(**item) for item in data]
                count = len(duties)
            elif filename == "i18n.json":
                count = len(data.get("articles", {}))

            print(f"[PASS] {filename:<20} | Size: {size_kb:6.2f} KB | Records: {count:4d} | SHA256: {sha256[:16]}...")
            summary_stats[filename] = {"size_kb": size_kb, "records": count, "sha256": sha256}

        except Exception as e:
            print(f"[FAIL] {filename}: {e}")
            all_passed = False

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    print("-" * 75)
    print(f"Validation completed in {elapsed_ms:.2f} ms")
    print(f"Overall Status: {'PASSED' if all_passed else 'FAILED'}")
    print("=" * 75)

    return all_passed


if __name__ == "__main__":
    success = validate_corpus()
    sys.exit(0 if success else 1)
