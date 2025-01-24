from indianconstitution import (
    IndianConstitution,
    get_preamble,
    get_article,
    list_articles,
    search_keyword,
    get_article_summary,
    count_total_articles,
    search_by_title,
)

def main():
    # Initialize the IndianConstitution instance
    constitution_data_file = "constitution_data.json"  # Update with your actual JSON file path
    indian_const = IndianConstitution(constitution_data_file)

    print("Welcome to the Indian Constitution Explorer!")
    print("Choose an option:")
    print("1. View the Preamble")
    print("2. Get details of an Article")
    print("3. List all Articles")
    print("4. Search Constitution by Keyword")
    print("5. Get a Summary of an Article")
    print("6. Count Total Articles")
    print("7. Search Articles by Title")
    print("0. Exit")

    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            
            if choice == 0:
                print("Exiting the Indian Constitution Explorer. Goodbye!")
                break
            elif choice == 1:
                print("\nPreamble:")
                print(get_preamble(indian_const))
            elif choice == 2:
                article_num = int(input("Enter the Article number: "))
                print("\nArticle Details:")
                print(get_article(indian_const, article_num))
            elif choice == 3:
                print("\nList of Articles:")
                print(list_articles(indian_const))
            elif choice == 4:
                keyword = input("Enter a keyword to search: ")
                print("\nSearch Results:")
                print(search_keyword(indian_const, keyword))
            elif choice == 5:
                article_num = int(input("Enter the Article number: "))
                print("\nArticle Summary:")
                print(get_article_summary(indian_const, article_num))
            elif choice == 6:
                total_articles = count_total_articles(indian_const)
                print(f"\nTotal number of Articles: {total_articles}")
            elif choice == 7:
                title_keyword = input("Enter a keyword for the title search: ")
                print("\nSearch Results:")
                print(search_by_title(indian_const, title_keyword))
            else:
                print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid input. Please enter a number.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
