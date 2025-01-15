# iconlib <small> (v0.1) </small>
Python module to interact with the Constitution of India data and retrieve articles, details, summaries, and search functionalities.

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/iconlib?label=Python) ![PyPI - License](https://img.shields.io/pypi/l/iconlib?label=License&color=red) ![Maintenance](https://img.shields.io/maintenance/yes/2025?label=Maintained) ![PyPI](https://img.shields.io/pypi/v/iconlib?label=PyPi) ![PyPI - Status](https://img.shields.io/pypi/status/iconlib?label=Status)

## Installation
You can install it using pip from the repository as:

    pip install iconlib

## Usage
Iconlib can be used as a Python module to interact with the Constitution of India data.

### Python Module Usage
Here are examples of all current features:

```python
    >>> from iconlib import IconLib
    >>> india = IconLib()
    >>> india.preamble()
    'We, the people of India, having solemnly resolved to constitute India into a Sovereign, Socialist, Secular, Democratic Republic...'
    >>> india.get_article(14)
    'Article 14: Equality before law. The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.'
    >>> india.articles_list()
    'Article 14: Equality before law\nArticle 15: Prohibition of discrimination on grounds of religion, race, caste, sex or place of birth\n...'
    >>> india.search_keyword('equality')
    'Article 14: Equality before law. The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.'
    >>> india.article_summary(21)
    'Article 21: Protection of life and personal liberty. No person shall be deprived of his life or personal liberty except according to procedure established by law.'
    >>> india.count_articles()
    448
    >>> india.search_by_title('Fundamental')
    'Article 12: Definition of State\nArticle 13: Laws inconsistent with or in derogation of the fundamental rights\n...'
```
## license
This project is released under the Apache License 2.0.

The Constitution data is compiled from publicly available sources.

constitution_of_india.json

## Developer Information
Developer: Vikhram S.
Email: vikhrams@saveetha.ac.in
