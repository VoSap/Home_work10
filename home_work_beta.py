from collections import UserDict


class Field:
    pass


class Name(Field):
    def __init__(self, name):
        self.name = name


class Phone(Field):
    def __init__(self, phone):
        self.phone = phone


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.phone == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.phone == old_phone:
                p.phone = new_phone


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.HANDLERS = {
            'hello': self.hello,
            'add': self.add_user,
            'change': self.change_phone,
            'show_all': self.show_all,
            'phone': self.show_phone,
            'exit': self.exit,
            'goodbye': self.exit,
            'close': self.exit,
        }

    def add_record(self, record):
        self.data[record.name.name] = record

    def hello(self, _):
        return "How can I help you?"

    def unknown_command(self, _):
        return "Unknown command"

    def exit(self, _):
        return None

    def add_user(self, args):
        try:
            name, phone = args
        except ValueError:
            return 'Give me name and phone please'

        record = Record(name)
        record.add_phone(phone)
        self.add_record(record)
        return f'User {name} added!'

    def change_phone(self, args):
        try:
            name, phone = args
        except ValueError:
            return 'Give me name and phone please'

        if name in self.data:
            record = self.data[name]
            old_phone = record.phones[0].phone
            record.edit_phone(old_phone, phone)
            return f'{name} now has a phone: {phone}. The old number: {old_phone}'
        else:
            return 'No user'

    def show_all(self, _):
        if not self.data:
            return 'Address book is empty'
        result = 'All contacts:\n'
        for name, record in self.data.items():
            phones = [p.phone for p in record.phones]
            result += f'Name: {record.name.name}, Phones: {", ".join(phones)}\n'
        return result

    def show_phone(self, args):
        try:
            name = args[0]
        except IndexError:
            return 'Enter user name'

        if name in self.data:
            record = self.data[name]
            phones = [p.phone for p in record.phones]
            return f'User: {name}. Mobile: {", ".join(phones)}'
        else:
            return 'No user'

    def parse_input(self, user_input):
        command, *args = user_input.split()
        command = command.lower()
        try:
            handler = self.HANDLERS[command]
        except KeyError:
            if args:
                command = command + ' ' + args[0]
                args = args[1:]
            handler = self.unknown_command
        return handler, args

    def main(self):
        while True:
            user_input = input('Please enter command and args: ')
            handler, args = self.parse_input(user_input.strip())
            result = handler(args)
            if handler == self.exit:
                print('Good bye!')
                break
            elif result is not None:
                print(result)


if __name__ == "__main__":
    address_book = AddressBook()
    address_book.main()