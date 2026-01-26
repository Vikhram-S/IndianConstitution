"""
IndianConstitution: A Python module for accessing and managing Constitution data.
This module provides functionality to retrieve articles, search keywords, 
list articles, and more, using hardcoded Constitution data within the IndianConstitution class.
"""

from typing import Union
from .indianconstitution import IndianConstitution

# Metadata
__title__ = 'IndianConstitution'
__version__ = '0.8'
__author__ = 'Vikhram S'
__license__ = 'Apache License 2.0'

# Exported symbols for `from IndianConstitution import *`
__all__ = [
    'IndianConstitution',
    'get_preamble',
    'get_article',
    'list_articles',
    'search_keyword',
    'get_article_summary',
    'count_total_articles',
    'search_by_title',
    # Advanced features
    'to_dataframe',
    'filter',
    'search_regex',
    'fuzzy_search',
    'find_related_articles',
    'export_json',
    'export_csv',
    'export_markdown',
    'get_statistics',
    'visualize_word_frequency',
    'get_articles_by_part',
    'batch_get_articles',
]

# Convenience functions
def get_preamble() -> str:
    """Retrieve the Preamble of the Constitution."""
    instance = IndianConstitution()
    return instance.preamble()

def get_article(number: Union[int, str]) -> str:
    """
    Retrieve the details of a specific article.
    
    Args:
        number: The article number, which can be an integer (e.g., 41) or string (e.g., '41A').
    
    Returns:
        A string containing the article's details.
    
    Raises:
        ValueError: If the article number is not an integer or string.
    """
    if not isinstance(number, (int, str)):
        raise ValueError("Article number must be an integer or string.")
    number_str = str(number)
    instance = IndianConstitution()
    return instance.get_article(number_str)

def list_articles() -> str:
    """List all articles in the Constitution."""
    instance = IndianConstitution()
    return instance.articles_list()

def search_keyword(keyword: str) -> str:
    """
    Search for a keyword in the Constitution.
    
    Args:
        keyword: The keyword to search for.
    
    Returns:
        A string containing search results.
    
    Raises:
        ValueError: If the keyword is not a string.
    """
    if not isinstance(keyword, str):
        raise ValueError("Keyword must be a string.")
    instance = IndianConstitution()
    return instance.search_keyword(keyword)

def get_article_summary(number: Union[int, str]) -> str:
    """
    Provide a brief summary of the specified article.
    
    Args:
        number: The article number, which can be an integer (e.g., 41) or string (e.g., '41A').
    
    Returns:
        A string containing the article's summary.
    
    Raises:
        ValueError: If the article number is not an integer or string.
    """
    if not isinstance(number, (int, str)):
        raise ValueError("Article number must be an integer or string.")
    number_str = str(number)
    instance = IndianConstitution()
    return instance.article_summary(number_str)

def count_total_articles() -> int:
    """Count the total number of articles in the Constitution."""
    instance = IndianConstitution()
    return instance.count_articles()

def search_by_title(title_keyword: str) -> str:
    """
    Search for articles by title keyword.
    
    Args:
        title_keyword: The keyword to search for in article titles.
    
    Returns:
        A string containing matching articles.
    
    Raises:
        ValueError: If the title keyword is not a string.
    """
    if not isinstance(title_keyword, str):
        raise ValueError("Title keyword must be a string.")
    instance = IndianConstitution()
    return instance.search_by_title(title_keyword)