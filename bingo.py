from dateutil import parser
import pickle
import sys


class Book:
    def __init__(self, name, author, read, applicableCategories):
        self.name = name
        self.author = author
        self.dateRead = parser.parse(read)
        self.applicableCategories = applicableCategories

    def updateDateRead(self, read):
        self.dateRead = parser.parse(read)

    def setApplicableCategories(self, categories):
        prompt = "Enter the categories that are applicable to this book.\n" + self.__repr__() + '\n'
        i = 0
        for category in categories:
            prompt += str(i) + '. ' + category + '\n'
            i += 1
        applicableCategories = raw_input(prompt)
        applicableCategories = list(map(int, applicableCategories.strip().replace(' ', '').split(',')))
        self.applicableCategories = applicableCategories

    def __repr__(self):
        return self.name + ", by " + self.author + ". Read on " + self.dateRead.date().strftime("%Y-%m-%d")


def loadCategories(path):
    categories = []
    with open(path) as f:
        for line in f:
            categories.append(line.strip())
    return categories


def loadBooks(path):
    f = open(path, 'r')
    books = []
    while True:
        try:
            name = f.readline().strip()
            author = f.readline().strip()
            read = f.readline().strip()
            applicableCategories = list(map(int, f.readline().strip()[1:-1].replace(' ', '').split(',')))
            books.append(Book(name, author, read, applicableCategories))
        except:
            f.close()
            return books


def storeBooks(books, path):
    f = open(path, 'w')
    for book in books:
        f.write(book.name + '\n')
        f.write(book.author + '\n')
        f.write(str(book.dateRead.date().strftime("%Y-%m-%d")) + '\n')
        f.write(str(book.applicableCategories) + '\n')
    f.close()


def showBooks(books):
    for i in range(len(books)):
        print(str(i) + '. ' + str(books[i]))


def printCard(books, categories, card):
    for square in card:
        category = square
        book = books[card[square]]
        print(categories[category])
        print(books[book])


def interface():
    catFile = 'categories.txt'
    bookFile = 'books.txt'
    cardFile = 'card.pickle'
    prompt = """Usage:
    1. Add new book.
    2. Edit book categories.
    3. Set a book to a square.
    4. See current books.
    5. See current bingo card.
    6. Exit.
    """

    categories = loadCategories(catFile)
    books = loadBooks(bookFile)

    f = open(cardFile, 'rb')
    card = pickle.load(f)
    f.close()

    while True:
        option = raw_input(prompt)

        if option not in ['1', '2', '3', '4', '5', '6']:
            print(option + " is not a valid option. Please select a valid option.")
        elif option == '1':
            name = raw_input("Name of the book?")
            author = raw_input("Name of the author?")
            dateRead = raw_input("Date you read the book?")
            newBook = Book(name, author, dateRead, [])
            print(newBook)
            newBook.setApplicableCategories(categories)
            books.append(newBook)
        elif option == '2':
            showBooks(books)
            bookNum = int(raw_input("Which book would you like to update?"))
            books[bookNum].setApplicableCategories(categories);
        elif option == '3':
            s = ""
            for i in range(len(categories)):
                s += "Category: " + categories[i] + "\n"
                s += "Applicable books: "
                for j in range(len(books)):
                    if i in books[j].applicableCategories:
                        s += str(j) + ". " + books[j].name + ". "
                s += "\nThe currrently set book for this square is "
                if i in card.keys():
                    s += books[card[i]].name + '\n'
                else:
                    s += 'N\A.\n'
            print(s)
            catNumber = int(raw_input("Choose category number."))
            bookNum = int(raw_input("Choose book number."))
            if catNumber in books[bookNum].applicableCategories:
                card[catNumber] = bookNum
            else:
                print("Invalid selection. The selected book is not eligible for the selected square.")
        elif option == '4':
            showBooks(books)
        elif option == '5':
            printCard(books, categories, card)
        else:
            f = open(cardFile, 'wb')
            pickle.dump(card, f)
            f.close()
            storeBooks(books, bookFile)
            print("Goodbye!")
            sys.exit()


interface()
