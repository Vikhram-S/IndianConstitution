#!/usr/bin/env python3
"""
Command-line interface for IndianConstitution library.
Provides easy access to Constitution data from the terminal.
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional

try:
    from .indianconstitution import IndianConstitution
except ImportError:
    from indianconstitution import IndianConstitution


def print_article(constitution: IndianConstitution, article_num: str):
    """Print a specific article."""
    result = constitution.get_article(article_num)
    print(result)


def search_articles(constitution: IndianConstitution, keyword: str, fuzzy: bool = False):
    """Search for articles by keyword."""
    if fuzzy:
        try:
            results = constitution.fuzzy_search(keyword)
            if results:
                print(f"\nFound {len(results)} articles (fuzzy search):\n")
                for article in results:
                    print(f"Article {article['article']}: {article['title']}")
            else:
                print("No articles found.")
        except ImportError:
            print("Error: fuzzywuzzy is required for fuzzy search.")
            print("Install with: pip install indianconstitution[fuzzy]")
            sys.exit(1)
    else:
        result = constitution.search_keyword(keyword)
        print(result)


def export_data(constitution: IndianConstitution, format_type: str, output: str):
    """Export constitution data to a file."""
    output_path = Path(output)
    
    try:
        if format_type == 'json':
            constitution.export_json(output_path)
            print(f"✓ Exported to {output_path}")
        elif format_type == 'csv':
            constitution.export_csv(output_path)
            print(f"✓ Exported to {output_path}")
        elif format_type == 'markdown':
            constitution.export_markdown(output_path)
            print(f"✓ Exported to {output_path}")
        else:
            print(f"Error: Unsupported format '{format_type}'")
            sys.exit(1)
    except ImportError as e:
        print(f"Error: {e}")
        print("Install required dependencies with: pip install indianconstitution[all]")
        sys.exit(1)
    except Exception as e:
        print(f"Error exporting: {e}")
        sys.exit(1)


def show_statistics(constitution: IndianConstitution):
    """Display statistics about the Constitution."""
    stats = constitution.get_statistics()
    print("\n" + "="*50)
    print("CONSTITUTION OF INDIA - STATISTICS")
    print("="*50)
    print(f"Total Articles: {stats['total_articles']}")
    print(f"Total Words: {stats['total_words']:,}")
    print(f"Total Characters: {stats['total_characters']:,}")
    print(f"Average Words per Article: {stats['average_words_per_article']}")
    print(f"\nLongest Article:")
    print(f"  Article {stats['longest_article']['number']}: {stats['longest_article']['title']}")
    print(f"  Word Count: {stats['longest_article']['word_count']}")
    print(f"\nShortest Article:")
    print(f"  Article {stats['shortest_article']['number']}: {stats['shortest_article']['title']}")
    print(f"  Word Count: {stats['shortest_article']['word_count']}")
    print("="*50)


def show_preamble(constitution: IndianConstitution):
    """Display the Preamble."""
    print("\n" + "="*50)
    print("PREAMBLE TO THE CONSTITUTION OF INDIA")
    print("="*50)
    print(constitution.preamble())
    print("="*50)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='IndianConstitution CLI - Access the Constitution of India from your terminal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Get a specific article
  indianconstitution get 14
  
  # Search for articles
  indianconstitution search equality
  
  # Fuzzy search
  indianconstitution search --fuzzy "fundamental rights"
  
  # Export to JSON
  indianconstitution export json constitution.json
  
  # Show statistics
  indianconstitution stats
  
  # Show preamble
  indianconstitution preamble
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Get article command
    get_parser = subparsers.add_parser('get', help='Get a specific article')
    get_parser.add_argument('article', help='Article number (e.g., 14, 21A)')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search for articles')
    search_parser.add_argument('keyword', help='Keyword to search for')
    search_parser.add_argument('--fuzzy', action='store_true', help='Use fuzzy search')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export data to file')
    export_parser.add_argument('format', choices=['json', 'csv', 'markdown'], help='Export format')
    export_parser.add_argument('output', help='Output file path')
    
    # Statistics command
    stats_parser = subparsers.add_parser('stats', help='Show statistics about the Constitution')
    
    # Preamble command
    preamble_parser = subparsers.add_parser('preamble', help='Display the Preamble')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Initialize constitution
    constitution = IndianConstitution()
    
    # Execute command
    if args.command == 'get':
        print_article(constitution, args.article)
    elif args.command == 'search':
        search_articles(constitution, args.keyword, args.fuzzy)
    elif args.command == 'export':
        export_data(constitution, args.format, args.output)
    elif args.command == 'stats':
        show_statistics(constitution)
    elif args.command == 'preamble':
        show_preamble(constitution)


if __name__ == '__main__':
    main()
