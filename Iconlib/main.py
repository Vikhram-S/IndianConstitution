from iconlib import IconLib

def main():
    """
    Main function to initialize and run the IconLib module.
    """
    try:
        # Initialize the IconLib with default data file
        india = IconLib()

        # You can now use any method from IconLib class.
        print("IconLib initialized successfully.")

        # Example: Get the Preamble of the Constitution
        print("Preamble of the Constitution:")
        print(india.preamble())

        # Example: Get details of Article 14
        print("\nArticle 14 Details:")
        print(india.get_article(14))

        # Example: List all articles
        print("\nList of Articles:")
        print(india.articles_list())

        # Example: Search for the keyword "equality"
        print("\nSearch results for 'equality':")
        print(india.search_keyword("equality"))

        # Example: Get article summary of Article 21
        print("\nSummary of Article 21:")
        print(india.article_summary(21))

        # Example: Count total number of articles
        print("\nTotal Number of Articles:")
        print(india.count_articles())

        # Example: Search articles by title containing "Fundamental"
        print("\nSearch results for 'Fundamental' in article titles:")
        print(india.search_by_title("Fundamental"))

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
