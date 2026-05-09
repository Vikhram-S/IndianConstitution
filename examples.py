"""
Advanced Examples for IndianConstitution Library
Demonstrates all the new features in v0.8
"""

from indianconstitution import IndianConstitution

def example_basic_usage():
    """Basic usage examples."""
    print("="*60)
    print("BASIC USAGE EXAMPLES")
    print("="*60)
    
    india = IndianConstitution()
    
    # Get preamble
    print("\n1. Preamble:")
    print(india.preamble()[:200] + "...")
    
    # Get specific article
    print("\n2. Article 14:")
    print(india.get_article(14))
    
    # Count articles
    print(f"\n3. Total Articles: {india.count_articles()}")
    
    # Search
    print("\n4. Search for 'equality':")
    results = india.search_keyword('equality')
    print(results[:500] + "..." if len(results) > 500 else results)


def example_dataframe():
    """DataFrame examples (requires pandas)."""
    print("\n" + "="*60)
    print("DATAFRAME EXAMPLES")
    print("="*60)
    
    try:
        import pandas as pd
        india = IndianConstitution()
        
        # Convert to DataFrame
        df = india.to_dataframe()
        
        print("\n1. DataFrame Info:")
        print(df.info())
        
        print("\n2. First 5 Articles:")
        print(df.head()[['article', 'title', 'word_count']])
        
        print("\n3. Articles with most words:")
        top_longest = df.nlargest(5, 'word_count')
        print(top_longest[['article', 'title', 'word_count']])
        
        print("\n4. Articles containing 'Fundamental' in title:")
        fundamental = df[df['title'].str.contains('Fundamental', case=False, na=False)]
        print(fundamental[['article', 'title']])
        
        print("\n5. Statistics:")
        print(df.describe())
        
    except ImportError:
        print("\n⚠ pandas not installed. Install with: pip install pandas")


def example_advanced_search():
    """Advanced search examples."""
    print("\n" + "="*60)
    print("ADVANCED SEARCH EXAMPLES")
    print("="*60)
    
    india = IndianConstitution()
    
    # Regex search
    print("\n1. Regex Search (finding articles with 'equality' or 'liberty'):")
    results = india.search_regex(r'\b(equality|liberty)\b', case_sensitive=False)
    print(f"Found {len(results)} articles:")
    for article in results[:5]:  # Show first 5
        print(f"  - Article {article['article']}: {article['title']}")
    
    # Fuzzy search
    print("\n2. Fuzzy Search (handles typos):")
    try:
        results = india.fuzzy_search('fundamental rights', threshold=70, limit=5)
        print(f"Found {len(results)} articles:")
        for article in results:
            print(f"  - Article {article['article']}: {article['title']}")
    except ImportError:
        print("⚠ fuzzywuzzy not installed. Install with: pip install fuzzywuzzy")


def example_export():
    """Export examples."""
    print("\n" + "="*60)
    print("EXPORT EXAMPLES")
    print("="*60)
    
    india = IndianConstitution()
    
    # Export to JSON
    print("\n1. Exporting to JSON...")
    try:
        india.export_json('constitution_example.json')
        print("✓ Exported to constitution_example.json")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Export to CSV
    print("\n2. Exporting to CSV...")
    try:
        india.export_csv('constitution_example.csv')
        print("✓ Exported to constitution_example.csv")
    except ImportError:
        print("⚠ pandas not installed. Install with: pip install pandas")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Export to Markdown
    print("\n3. Exporting to Markdown...")
    try:
        india.export_markdown('constitution_example.md')
        print("✓ Exported to constitution_example.md")
    except Exception as e:
        print(f"✗ Error: {e}")


def example_statistics():
    """Statistics examples."""
    print("\n" + "="*60)
    print("STATISTICS EXAMPLES")
    print("="*60)
    
    india = IndianConstitution()
    
    stats = india.get_statistics()
    
    print("\nConstitution Statistics:")
    print(f"  Total Articles: {stats['total_articles']}")
    print(f"  Total Words: {stats['total_words']:,}")
    print(f"  Total Characters: {stats['total_characters']:,}")
    print(f"  Average Words per Article: {stats['average_words_per_article']}")
    print(f"\n  Longest Article:")
    print(f"    Article {stats['longest_article']['number']}: {stats['longest_article']['title']}")
    print(f"    Word Count: {stats['longest_article']['word_count']}")
    print(f"\n  Shortest Article:")
    print(f"    Article {stats['shortest_article']['number']}: {stats['shortest_article']['title']}")
    print(f"    Word Count: {stats['shortest_article']['word_count']}")


def example_relationships():
    """Relationship mapping examples."""
    print("\n" + "="*60)
    print("RELATIONSHIP MAPPING EXAMPLES")
    print("="*60)
    
    india = IndianConstitution()
    
    # Find articles that reference Article 14
    print("\n1. Articles that reference Article 14:")
    related = india.find_related_articles(14, max_results=10)
    print(f"Found {len(related)} articles:")
    for article in related:
        print(f"  - Article {article['article']}: {article['title']}")
    
    # Find articles that reference Article 21
    print("\n2. Articles that reference Article 21:")
    related = india.find_related_articles(21, max_results=10)
    print(f"Found {len(related)} articles:")
    for article in related:
        print(f"  - Article {article['article']}: {article['title']}")


def example_method_chaining():
    """Method chaining examples."""
    print("\n" + "="*60)
    print("METHOD CHAINING EXAMPLES")
    print("="*60)
    
    india = IndianConstitution()
    
    # Filter and search
    print("\n1. Filter articles with 'rights' in title, then search for 'equality':")
    filtered = india.filter(lambda art: 'rights' in art.get('title', '').lower())
    results = filtered.search_keyword('equality')
    print(results[:500] + "..." if len(results) > 500 else results)


def example_dictionary_access():
    """Dictionary-like access examples."""
    print("\n" + "="*60)
    print("DICTIONARY-LIKE ACCESS EXAMPLES")
    print("="*60)
    
    india = IndianConstitution()
    
    # Access like dictionary
    print("\n1. Access Article 14 like a dictionary:")
    article_14 = india[14]
    print(f"  Title: {article_14['title']}")
    print(f"  Description (first 100 chars): {article_14['description'][:100]}...")
    
    # Get length
    print(f"\n2. Total articles: {len(india)}")
    
    # Iterate
    print("\n3. First 5 articles:")
    for i, article in enumerate(india):
        if i >= 5:
            break
        print(f"  Article {article['article']}: {article['title']}")


def example_batch_operations():
    """Batch operations examples."""
    print("\n" + "="*60)
    print("BATCH OPERATIONS EXAMPLES")
    print("="*60)
    
    india = IndianConstitution()
    
    # Get multiple articles at once
    print("\n1. Get multiple articles at once:")
    articles = india.batch_get_articles([14, 15, 16, 21, 21])
    for article in articles:
        print(f"  Article {article['article']}: {article['title']}")


def example_grouping():
    """Grouping examples."""
    print("\n" + "="*60)
    print("GROUPING EXAMPLES")
    print("="*60)
    
    india = IndianConstitution()
    
    # Group by parts
    print("\n1. Group articles by parts:")
    parts = india.get_articles_by_part()
    for part_name, articles in parts.items():
        print(f"  {part_name}: {len(articles)} articles")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("INDIAN CONSTITUTION LIBRARY - ADVANCED EXAMPLES")
    print("="*60)
    
    example_basic_usage()
    example_dataframe()
    example_advanced_search()
    example_export()
    example_statistics()
    example_relationships()
    example_method_chaining()
    example_dictionary_access()
    example_batch_operations()
    example_grouping()
    
    print("\n" + "="*60)
    print("EXAMPLES COMPLETED!")
    print("="*60)
    print("\nFor more information, visit: https://github.com/Vikhram-S/IndianConstitution")


if __name__ == '__main__':
    main()
