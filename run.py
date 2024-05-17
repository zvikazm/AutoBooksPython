import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_session():
    username = "זמיריא"
    password = "זמיריא"

    # URL for login
    login_url = "https://kedumim.libraries.co.il/BuildaGate5library/general2/xaction.php?ActionID=1"
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

    return session


def get_current_loaned_books_page(session):
    target_url = "https://kedumim.libraries.co.il/BuildaGate5library/general/library_user_report_personal.php?SiteName=LIB_kedumim&CNumber=318119515&Clubtmp1=5SKNQWLVRU86B861&lan=en&ItemID=318119515&TPLItemID=&Card=Card6"
    response_books = session.get(target_url)
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
    print(f"found {len(books)} books:")
    for book in books:
        print(book)


def get_history(session):
    # history_url = "https://kedumim.libraries.co.il/BuildaGate5library/controllers/userHistory.php?toDate2=&fromDate1=&toDate4=&fromDate3=&toDate6=&fromDate5=&ord=&numOfPages=67&currentPage=2&numOfResultsInPage=50&UserItemNum=318119515&from=50&_=1715952263756"
    history_url = "https://kedumim.libraries.co.il/BuildaGate5library/controllers/userHistory.php?numOfResultsInPage=5000&UserItemNum=318119515"
    response_history = session.get(history_url)
    return response_history.text


def parse_history(history):
    soup = BeautifulSoup(history, 'html.parser')
    # with open("history.html", "w", encoding="utf-8") as f:
    #     f.write(soup.prettify())

    rows = soup.find_all('form')[0].find_all('th')[7].find_all('tr')
    print(f"found {len(rows)} rows")

    data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1:
            data.append([cell.text for cell in cells])



    df = pd.DataFrame(
        data, columns=["מספר", "שם הפריט", "שם המחבר", "בר קוד", "תאריך השאלה", "תאריך החזרה מיועד", "תאריך החזרה בפועל", "הערות"])
    df.to_csv("history.csv", index=False, encoding='utf-8-sig')


def main():
    session = get_session()
    # current_loan_books = get_current_loaned_books_page(session)
    # parse_page(current_loan_books)
    history = get_history(session)
    parse_history(history)


if __name__ == '__main__':
    main()
