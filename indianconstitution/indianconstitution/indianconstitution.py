import json
import os
import re
from typing import List, Dict, Union

class IndianConstitution:
    def __init__(self, data_file: str = 'constitution_of_india.json'):
        """
        Initialize the IndianConstitution class and load the data.
        :param data_file: Path to the JSON file containing the Constitution data.
        """
        self.data = self._load_data(data_file)

    @staticmethod
    def _load_data(file_path: str) -> List[Dict]:
        """
        Load constitution data from the JSON file.
        :param file_path: Path to the JSON file.
        :return: List containing the data from the JSON file.
        """
        abs_path = os.path.join(os.path.dirname(__file__), file_path)
        try:
            with open(abs_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in the file.")

    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean the input text by removing unwanted characters and excess spaces."""
        return re.sub(r'(\xa0|\{}|\n|\t|\s{2,})', ' ', text).strip()

    def preamble(self) -> str:
        """
        Retrieve the Preamble of the Constitution.
        :return: Preamble text.
        """
        preamble = next((article.get("description") for article in self.data if article.get("article") == 0), None)
        return self._clean_text(preamble) if preamble else "Preamble not found."

    def get_article(self, number: Union[int, str]) -> str:
        """
        Retrieve the details of a specific article.
        :param number: Article number to retrieve.
        :return: Formatted string containing article details or a message if not found.
        """
        article = next((art for art in self.data if str(art.get("article")) == str(number)), None)
        if article:
            article["description"] = self._clean_text(article.get("description", ""))
            return f"Article {article['article']}: {article['title']}. {article['description']}"
        return "Article not found."

    def articles_list(self) -> str:
        """
        List all articles in the Constitution in a readable string format.
        :return: String listing article numbers and titles.
        """
        return '\n'.join([f"Article {article.get('article')}: {self._clean_text(article.get('title', ''))}" for article in self.data if article.get("article")])

    def search_keyword(self, keyword: str) -> str:
        """
        Search for a keyword in the Constitution.
        :param keyword: The keyword to search for.
        :return: String containing articles with the keyword or a message if none found.
        """
        keyword_lower = keyword.lower()
        results = []
        for article in self.data:
            if keyword_lower in article.get("description", "").lower() or keyword_lower in article.get("title", "").lower():
                article_copy = article.copy()
                article_copy["description"] = self._clean_text(article_copy.get("description", ""))
                results.append(f"Article {article_copy['article']}: {article_copy['title']}. {article_copy['description']}")
        return '\n'.join(results) if results else "No articles found containing the keyword."

    def article_summary(self, number: Union[int, str]) -> str:
        """
        Provide a brief summary of the specified article.
        :param number: Article number to summarize.
        :return: Summary text or a not found message.
        """
        article = self.get_article(number)
        if "Article not found" not in article:
            # Fixed splitting issue for a proper summary
            description_start = article.split('.')[2][:100] if len(article.split('.')) > 2 else ""
            return f"{article.split('.')[0]} - {description_start.strip()}..."
        return article

    def count_articles(self) -> int:
        """
        Count the total number of articles in the Constitution.
        :return: Number of articles.
        """
        return len([article for article in self.data if article.get("article")])

    def search_by_title(self, title_keyword: str) -> str:
        """
        Search for articles by title keyword.
        :param title_keyword: Keyword to search in article titles.
        :return: String of matching articles or a message if none found.
        """
        title_keyword_lower = title_keyword.lower()
        results = [
            f"Article {article['article']}: {article['title']}" for article in self.data if title_keyword_lower in article.get("title", "").lower()
        ]
        return '\n'.join(results) if results else "No articles found with the given title keyword."

# Example usage and syntax for users
if __name__ == "__main__":
    # Direct usage without creating an object
    india = IndianConstitution()  # Instantiation still required for accessing methods
    
    try:
        # 1. Get Preamble
        print("Preamble:", india.preamble())

        # 2. Get details of a specific article
        print("Article 14 Details:", india.get_article(14))

        # 3. List all articles
        print("List of Articles:\n", india.articles_list())

        # 4. Search for articles by keyword
        print("Search for 'equality':\n", india.search_keyword("equality"))

        # 5. Get a brief summary of an article
        print("Article 21 Summary:", india.article_summary(21))

        # 6. Count total number of articles
        print("Total Number of Articles:", india.count_articles())

        # 7. Search articles by title keyword
        print("Search Articles by Title 'Fundamental':\n", india.search_by_title("Fundamental"))

    except Exception as e:
        print(f"An error occurred: {e}")
