# IconLib - A Python Library for the Constitution of India
IconLib is a Python library that allows users to explore, search, and interact with the Constitution of India. The library enables retrieval of the Preamble, detailed article descriptions, and allows for keyword-based searches across the Constitution. It provides methods for summarizing articles, listing all articles, and more.

# Features
Retrieve the Preamble of the Constitution.
Get detailed descriptions for any article by article number.
List all articles and their titles.
Search for articles containing a specific keyword in their title or description.
Get a brief summary of any article.
Count the total number of articles.
Search for articles by title keyword.
# Installation
Using pip (from GitHub)
You can install IconLib directly from GitHub using pip:

pip install git+https://github.com/yourusername/iconlib.git
From Source
Clone the repository and install manually:

bash
Copy code
git clone https://github.com/yourusername/iconlib.git
cd iconlib
python setup.py install
Usage
Basic Usage Example
Once IconLib is installed, you can start using the library as follows:

python
Copy code
from iconlib import IconLib

# Initialize the IconLib class with the path to your JSON file (optional)
india = IconLib()

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
Methods
__init__(self, data_file: str = 'constitution_of_india.json')
Parameters:
data_file (str): Path to the JSON file containing the Constitution data. Defaults to 'constitution_of_india.json'.
Description: Initializes the IconLib class and loads the data from the provided JSON file.
preamble(self) -> str
Returns: A string representing the Preamble of the Constitution.
Description: Retrieves the Preamble of the Constitution. Returns a default message if not found.
get_article(self, number: Union[int, str]) -> str
Parameters:
number (Union[int, str]): The article number (either an integer or string).
Returns: A formatted string with the article number, title, and description.
Description: Retrieves the details of a specific article based on the provided article number.
articles_list(self) -> str
Returns: A string listing all articles and their titles in the Constitution.
Description: Lists all articles in the Constitution in a human-readable format.
search_keyword(self, keyword: str) -> str
Parameters:
keyword (str): The keyword to search for.
Returns: A string containing articles that match the keyword in their title or description.
Description: Searches for a keyword in the Constitution and returns matching articles.
article_summary(self, number: Union[int, str]) -> str
Parameters:
number (Union[int, str]): The article number to summarize.
Returns: A brief summary of the specified article.
Description: Provides a summary of the specified article, including the first 100 characters of its description.
count_articles(self) -> int
Returns: An integer representing the total number of articles in the Constitution.
Description: Returns the total number of articles in the Constitution.
search_by_title(self, title_keyword: str) -> str
Parameters:
title_keyword (str): The keyword to search for in the article titles.
Returns: A string of articles that match the keyword in their title.
Description: Searches for articles based on a title keyword and returns matching results.

# Data Format
The data is expected to be in a JSON format, with each article structured as follows:

json
Copy code
[
  {
    "article": 1,
    "title": "Short title and commencement",
    "description": "This article is about the short title and commencement of the Constitution."
  },
  {
    "article": 2,
    "title": "Admission of new States",
    "description": "This article deals with the admission of new states into the Union of India."
  },
  ...
]
# Each article should contain:

article: The article number (integer).
title: The title of the article (string).
description: The description of the article (string).
# License
This package is licensed under the MIT License. See the LICENSE file for more information.

# Contributing
Contributions to the IconLib project are welcome! If you have suggestions or improvements, feel free to fork the repository, make changes, and create a pull request. For large changes, please open an issue first to discuss what you would like to change.

# Contact
Author: Vikhram S
GitHub: Vikhram-S
Email: vikhrams@saveetha.ac.in
This template provides all the essential details for users to understand how to use the IconLib package, including method descriptions, usage examples, and information on how to install and contribute.






