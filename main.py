from address_book import AddressBook, Record
from storage import save_data, load_data

def input_error(func):

    def inner(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except ValueError:
            return "Give me name and phone please."

        except KeyError:
            return "Contact not found."

        except IndexError:
            return "Enter the argument for the command."

    return inner


def parse_input(user_input):

    cmd, *args = user_input.split()

    return cmd.lower(), args


@input_error
def add_contact(args, book):

    name, phone = args

    record = book.find(name)

    message = "Contact updated."

    if record is None:

        record = Record(name)

        book.add_record(record)

        message = "Contact added."

    record.add_phone(phone)

    return message


@input_error
def change_contact(args, book):

    name, old_phone, new_phone = args

    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_phone(old_phone, new_phone)

    return "Phone updated."


@input_error
def show_phone(args, book):

    name = args[0]

    record = book.find(name)

    if record is None:
        raise KeyError

    return "; ".join(p.value for p in record.phones)


def show_all(args, book):

    if not book.data:
        return "No contacts."

    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):

    name, birthday = args

    record = book.find(name)

    if record is None:
        raise KeyError

    record.add_birthday(birthday)

    return "Birthday added."


@input_error
def show_birthday(args, book):

    name = args[0]

    record = book.find(name)

    if record is None:
        raise KeyError

    if record.birthday is None:
        return "Birthday not set."

    return record.birthday


def birthdays(args, book):

    users = book.get_upcoming_birthdays()

    if not users:
        return "No upcoming birthdays."

    return "\n".join(
        f"{user['name']} -> {user['congratulation_date']}"
        for user in users
    )


def help_command(args, book):

    return """
Commands:
hello
add [name] [phone]
change [name] [old_phone] [new_phone]
phone [name]
all
add-birthday [name] [DD.MM.YYYY]
show-birthday [name]
birthdays
help
exit / close
"""


def main():

    book = load_data()

    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "all": show_all,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": birthdays,
        "help": help_command
    }

    print("Welcome to the assistant bot!")
    print("Type 'help' to see commands.")

    while True:

        user_input = input("Enter command: ")

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        if command == "hello":
            print("How can I help you?")
            continue

        func = commands.get(command)

        if func:
            print(func(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()