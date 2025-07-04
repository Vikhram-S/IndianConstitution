# IndianConstitution <small> (v0.6.0) </small>
Python module to interact with the Constitution of India data and retrieve articles, details, summaries, and search functionalities.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/indianconstitution?label=Python) ![PyPI - License](https://img.shields.io/pypi/l/indianconstitution?label=License&color=red) ![Maintenance](https://img.shields.io/maintenance/yes/2025?label=Maintained) ![PyPI](https://img.shields.io/pypi/v/indianconstitution?label=PyPi) ![PyPI - Status](https://img.shields.io/pypi/status/indianconstitution?label=Status)
![PyPI - Downloads](https://img.shields.io/pypi/dm/indianconstitution?label=Monthly%20Downloads) 
![Total Downloads](https://static.pepy.tech/badge/indianconstitution?label=Total%20Downloads)

---

## Installation
You can install the package directly from PyPI:

```bash
pip install indianconstitution
```

---

## Features
The `indianconstitution` module provides:

- Full access to the Constitution of India data.
- Retrieval of individual articles and summaries.
- Keyword-based search for articles.
- Count of total articles and search by title functionality.

---

## Usage
Here is how to get started with `indianconstitution`:


**Example:**

```python
from indianconstitution import IndianConstitution

# Load the module with the correct path to the JSON file
india = IndianConstitution()

# Example usage
print(india.preamble())
```

### Python Module Example

```python
from indianconstitution import IndianConstitution

# Load the module with your Constitution data
india = IndianConstitution()

# Access the Preamble
print(india.preamble())

# Retrieve specific articles
print(india.get_article(14))  # Outputs details of Article 14

# List all articles
print(india.articles_list())

# Search for a keyword in the Constitution
print(india.search_keyword('equality'))

# Get a summary of an article
print(india.article_summary(21))

# Count the total number of articles
print(india.count_articles())

# Search articles by title
print(india.search_by_title('Fundamental'))
```

---

## Key Functionalities

| Function                | Description                                                   |
|-------------------------|---------------------------------------------------------------|
| `preamble()`            | Returns the Preamble of the Constitution of India.           |
| `get_article(number)`   | Retrieves the full content of the specified article.          |
| `articles_list()`       | Lists all articles in the Constitution with titles.           |
| `search_keyword(word)`  | Finds all occurrences of a specific keyword in the Constitution text. |
| `article_summary(num)`  | Returns a summary of the specified article.                   |
| `count_articles()`      | Counts the total number of articles in the Constitution.      |
| `search_by_title(title)`| Searches articles by their titles and returns matching results.|

---

## Development
This project is actively maintained. Contributions, suggestions, and feedback are welcome. Please refer to the LICENSE file for usage terms.

---

## License
This project is licensed under the Apache License 2.0.
See the LICENSE file for more details.

---

## Data Source
The Constitution data is compiled from publicly available resources, ensuring authenticity and accuracy.

---

## Developer Information
**Author**: Vikhram S  
**Email**: [vikhrams@saveetha.ac.in](mailto:vikhrams@saveetha.ac.in)

---

## Copyright
©2025 Vikhram S. All rights reserved.
