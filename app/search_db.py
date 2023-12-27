from thefuzz import process

def search_books(search_term: str, search_type: str, books: list):
    search_results = []

    if search_type == "title":
        search_list = [book.title for book in books]
    elif search_type == "description":
        search_list = [book.description for book in books]
    elif search_type == "author":
        search_list = [book.author for book in books]

    while True:
        result = process.extractOne(search_term, search_list)

        if result is None or result[1] < 50:
            break

        search_results.append(result[0])
        search_list.remove(result[0])
    
    if search_type == "title":
        search_results = [book for book in books if book.title in search_results]
    elif search_type == "description":
        search_results = [book for book in books if book.description in search_results]
    elif search_type == "author":
        search_results = [book for book in books if book.author in search_results]

    return search_results

