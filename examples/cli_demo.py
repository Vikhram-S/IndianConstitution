"""CLI Demo — IndianConstitution Library.

Demonstrates using the command-line interface programmatically.
In practice, just use the CLI directly:

    indianconstitution get 21A
    indianconstitution search "equality before law"
    indianconstitution stats
    indianconstitution preamble
    indianconstitution related 32
    indianconstitution export json constitution.json
"""

import subprocess

commands = [
    ["indianconstitution", "get", "21A"],
    ["indianconstitution", "search", "equality", "--limit", "3"],
    ["indianconstitution", "stats"],
]

for cmd in commands:
    print(f"\n{'=' * 60}")
    print(f"  $ {' '.join(cmd)}")
    print(f"{'=' * 60}\n")
    subprocess.run(cmd, check=False)
