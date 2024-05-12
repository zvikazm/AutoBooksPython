import requests
from bs4 import BeautifulSoup


def get_books_page():
    username = "זמיריא"
    password = "זמיריא"

    # URL for login    
    login_url = "https://kedumim.libraries.co.il/BuildaGate5library/general2/xaction.php?ActionID=1"
    # URL for the page available after login
    target_url = "https://kedumim.libraries.co.il/BuildaGate5library/general/library_user_report_personal.php?SiteName=LIB_kedumim&CNumber=318119515&Clubtmp1=5SKNQWLVRU86B861&lan=en&ItemID=318119515&TPLItemID=&Card=Card6"
    # Create a session to persist cookies
    session = requests.Session()

    # Log in by sending a POST request with your credentials
    login_payload = {
        "PassID": username,
        "CodeID": password
    }

    try:
        login_response = session.post(login_url, data=login_payload)
        if login_response.status_code == 200:
            print("Login successful!")
        else:
            print(f"Login failed with status code {
                  login_response.status_code}")
    except Exception as e:
        print(f"Error during login: {e}")

    response_books = session.get(target_url)
    # with open("file.html", "w", encoding="utf-8") as f:
    #     f.write(response_books.text)

    return response_books.text
    
def parse_page(books_page):
    soup = BeautifulSoup(books_page, 'html.parser')
    tables = soup.find_all('table')
    loan_books_table = tables[3].find('table')
    rows = loan_books_table.find_all('tr')
    books = []
    for idx, row in enumerate(rows):
        cells = row.find_all('td')
        if len(cells) > 1:
            books.append(cells[1].text)
    
    # print all books in separate lines
    print (f"found {len(books)} books:")
    for book in books:
        print(book)




def main():
    books = get_books_page()
    parse_page(books)


if __name__ == '__main__':
    main()
