from pathlib import Path
import pickle
from address_book import AddressBook

BASE_DIR = Path(__file__).parent
FILE_PATH = BASE_DIR / "addressbook.pkl"

def save_data(book, filename=FILE_PATH):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename=FILE_PATH):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()