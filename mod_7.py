from collections import UserDict, defaultdict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
	pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if len(value) == 10 and value.isdigit():
            self.__value = value
        else:
            print("The number must consist of 10 digits")
            raise ValueError


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            print("Invalid date format. Use DD.MM.YYYY")
            raise ValueError
            
    
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, number):
        self.phones.append(Phone(number))
                  
    def remove_phone(self, number):
        for phone in self.phones:
            if str(phone) == number:
                self.phones.remove(phone)              
          
    def edit_phone(self, number, new_number):
        for phone in self.phones:
            if str(phone) == number:
                self.phones[self.phones.index(phone)] = Phone(new_number)             
        
    def find_phone(self, number):
        for phone in self.phones:
            if str(phone) == number:
                return phone
    
    def add_birthday(self, birthday):
         self.birthday = Birthday(birthday)
         
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
        def add_record(self, record):
            self.data[record.name.value] = record
        
        def find(self, name):
            return self.data.get(name)

        def delete(self, name):
            self.data.pop(name)

        def get_upcoming_birthdays(self, days=7):
            current_date = datetime.today().date()
            congratulation_period = timedelta(days)
            result = []
        
            for item in self.data:
                contact = self.data.get(item)
                birthday_dt = contact.birthday.date
                birthday_this_year = datetime(year=current_date.year,
                                              month=birthday_dt.month,
                                              day=birthday_dt.day).date()
                if birthday_this_year < current_date or birthday_this_year > current_date + congratulation_period:
                    continue
                congratulation_date = birthday_this_year
                if birthday_this_year.weekday() == 5:
                    congratulation_date = birthday_this_year + timedelta(days=2)
                if birthday_this_year.weekday() == 6:
                    congratulation_date = birthday_this_year + timedelta(days=1)
                result.append(f"Contact name: {contact.name}, birthday: {congratulation_date.strftime("%d.%m.%Y")}")
                  
            return result

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "This name is not in the contact list."
        except ValueError or IndexError:
            return "You must enter a name and a number or a birthday."
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact changed."
    else:
        raise KeyError

@input_error
def phone_from_contacts(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return record
    else:
        raise KeyError

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        raise KeyError

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    try:
        record = book.find(name)
        if record:
            return f"Contact name: {name}, birthday: {record.birthday.value}."
        else:
            raise KeyError
    except AttributeError:
        return f"No birthday given for {name}"

@input_error
def birthdays(args, book: AddressBook):
    try:
        birthdays_next_week = book.get_upcoming_birthdays()
        if len(birthdays_next_week) == 0:
            return None
        else:
            return birthdays_next_week
    except AttributeError:
        return None

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(phone_from_contacts(args, book))

        elif command == "all":
            for item in book:
                print(book.find(item))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            birthdays_nw = birthdays(args, book)
            if birthdays_nw:
                for bd in birthdays_nw:
                    print(bd)
            else:
                print("No birthdays next week")
            
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()