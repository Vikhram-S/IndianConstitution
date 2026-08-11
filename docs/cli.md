# Command Line Interface (CLI)

`indianconstitution` comes with a command-line interface powered by Typer and Rich.

## Commands Overview

| Command | Usage | Description |
|:---|:---|:---|
| `get` | `indianconstitution get <number>` | Retrieve and render a specific article |
| `search` | `indianconstitution search <query> [--limit N]` | Full-text inverted index keyword search |
| `preamble` | `indianconstitution preamble` | Render the Preamble with rich formatting |
| `related` | `indianconstitution related <number>` | Show cross-references for an article |
| `stats` | `indianconstitution stats` | Summary metrics (article count, word count) |
| `export` | `indianconstitution export <format> <output>` | Export corpus to JSON, CSV, or Markdown |

## Examples

### Retrieve Article 21A
```bash
indianconstitution get 21A
```

### Search Keywords
```bash
indianconstitution search "freedom of speech" --limit 5
```

### View Related Articles
```bash
indianconstitution related 32
```

### Export Dataset
```bash
indianconstitution export json output.json
indianconstitution export csv output.csv
```
