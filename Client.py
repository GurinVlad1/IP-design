import json


class ClientShort:
    @staticmethod
    def validate_client_id(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("client_id должен быть непустой строкой")

    @staticmethod
    def validate_name(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя/Фамилия должны быть непустой строкой")

    @staticmethod
    def validate_initials(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Инициалы должны быть непустой строкой")

    @staticmethod
    def validate_phone(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Телефон должен быть непустой строкой")

    def __init__(self, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                # Попытка парсинга как JSON
                try:
                    data = json.loads(arg)
                    client_id = data.get("client_id", "")
                    last_name = data.get("last_name", "")
                    initials = data.get("initials", "")
                    phone = data.get("phone", "")
                except json.JSONDecodeError:
                    # Парсинг как строка: client_id;last_name;initials;phone
                    parts = arg.split(';')
                    if len(parts) != 4:
                        raise ValueError("Неверный формат строки или JSON")
                    client_id = parts[0].strip()
                    last_name = parts[1].strip()
                    initials = parts[2].strip()
                    phone = parts[3].strip()
            elif isinstance(arg, dict):
                # Прямая передача dict (JSON-like)
                client_id = arg.get("client_id", "")
                last_name = arg.get("last_name", "")
                initials = arg.get("initials", "")
                phone = arg.get("phone", "")
            else:
                raise ValueError("Неверный тип аргумента для перегрузки")
        elif len(args) == 4:
            client_id, last_name, initials, phone = args
        else:
            raise ValueError("Неверное количество аргументов для ClientShort")

        # Валидация и инициализация
        self.validate_client_id(client_id)
        self.validate_name(last_name)
        self.validate_initials(initials)
        self.validate_phone(phone)
        self._client_id = client_id
        self._last_name = last_name
        self._initials = initials
        self._phone = phone

    @classmethod
    def from_string(cls, s):
        # Парсинг строки в формате: client_id;last_name;initials;phone
        parts = s.split(';')
        if len(parts) != 4:
            raise ValueError("Неверный формат строки")
        client_id = parts[0].strip()
        last_name = parts[1].strip()
        initials = parts[2].strip()
        phone = parts[3].strip()
        return cls(client_id, last_name, initials, phone)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        client_id = data.get("client_id", "")
        last_name = data.get("last_name", "")
        initials = data.get("initials", "")
        phone = data.get("phone", "")
        return cls(client_id, last_name, initials, phone)

    @classmethod
    def from_json_file(cls, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_str = f.read()
            return cls.from_json(json_str)
        except FileNotFoundError:
            raise ValueError(f"Файл {file_path} не найден")
        except json.JSONDecodeError:
            raise ValueError(f"Неверный JSON в файле {file_path}")

    def __str__(self):
        return f"ClientShort(client_id={self._client_id}, last_name={self._last_name}, initials={self._initials}, phone={self._phone})"

    def short_str(self):
        return f"{self._last_name} {self._initials} Тел: {self._phone}"

    # Перегрузка для сравнения
    def __eq__(self, other):
        if not isinstance(other, ClientShort):
            return False
        return (self._client_id == other._client_id and
                self._last_name == other._last_name and
                self._initials == other._initials and
                self._phone == other._phone)

    # Перегрузка для сравнения по client_id (меньше)
    def __lt__(self, other):
        if not isinstance(other, ClientShort):
            return NotImplemented
        return self._client_id < other._client_id

    @property
    def client_id(self):
        return self._client_id

    @client_id.setter
    def client_id(self, value):
        self.validate_client_id(value)
        self._client_id = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        self.validate_name(value)
        self._last_name = value

    @property
    def initials(self):
        return self._initials

    @initials.setter
    def initials(self, value):
        self.validate_initials(value)
        self._initials = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self.validate_phone(value)
        self._phone = value


class Client(ClientShort):
    def __init__(self, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                # Попытка парсинга как JSON
                try:
                    data = json.loads(arg)
                    client_id = data.get("client_id", "")
                    last_name = data.get("last_name", "")
                    first_name = data.get("first_name", "")
                    middle_name = data.get("middle_name", "")
                    address = data.get("address", "")
                    phone = data.get("phone", "")
                    initials = f"{first_name[0] if first_name else ''}.{middle_name[0] if middle_name else ''}."
                except json.JSONDecodeError:
                    # Парсинг как строка: client_id;last_name;first_name;middle_name;address;phone
                    parts = arg.split(';')
                    if len(parts) != 6:
                        raise ValueError("Неверный формат строки или JSON")
                    client_id = parts[0].strip()
                    last_name = parts[1].strip()
                    first_name = parts[2].strip()
                    middle_name = parts[3].strip()
                    address = parts[4].strip()
                    phone = parts[5].strip()
                    initials = f"{first_name[0] if first_name else ''}.{middle_name[0] if middle_name else ''}."
            elif isinstance(arg, dict):
                # Прямая передача dict (JSON-like)
                client_id = arg.get("client_id", "")
                last_name = arg.get("last_name", "")
                first_name = arg.get("first_name", "")
                middle_name = arg.get("middle_name", "")
                address = arg.get("address", "")
                phone = arg.get("phone", "")
                initials = f"{first_name[0] if first_name else ''}.{middle_name[0] if middle_name else ''}."
            else:
                raise ValueError("Неверный тип аргумента для перегрузки")
        elif len(args) == 6:
            client_id, last_name, first_name, middle_name, address, phone = args
            initials = f"{first_name[0] if first_name else ''}.{middle_name[0] if middle_name else ''}."
        else:
            raise ValueError("Неверное количество аргументов для Client")

        # Валидация и инициализация дополнительных полей
        self.validate_name(first_name)
        self.validate_name(middle_name)
        if not isinstance(address, str) or not address.strip():
            raise ValueError("Адрес должен быть непустой строкой")
        super().__init__(client_id, last_name, initials, phone)
        self._first_name = first_name
        self._middle_name = middle_name
        self._address = address

    @classmethod
    def from_string(cls, s):
        # Парсинг строки в формате: client_id;last_name;first_name;middle_name;address;phone
        parts = s.split(';')
        if len(parts) != 6:
            raise ValueError("Неверный формат строки")
        client_id = parts[0].strip()
        last_name = parts[1].strip()
        first_name = parts[2].strip()
        middle_name = parts[3].strip()
        address = parts[4].strip()
        phone = parts[5].strip()
        return cls(client_id, last_name, first_name, middle_name, address, phone)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        client_id = data.get("client_id", "")
        last_name = data.get("last_name", "")
        first_name = data.get("first_name", "")
        middle_name = data.get("middle_name", "")
        address = data.get("address", "")
        phone = data.get("phone", "")
        return cls(client_id, last_name, first_name, middle_name, address, phone)

    @classmethod
    def from_json_file(cls, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_str = f.read()
            return cls.from_json(json_str)
        except FileNotFoundError:
            raise ValueError(f"Файл {file_path} не найден")
        except json.JSONDecodeError:
            raise ValueError(f"Неверный JSON в файле {file_path}")

    def __str__(self):
        return (f"Client(client_id={self._client_id}, last_name={self._last_name}, first_name={self._first_name}, "
                f"middle_name={self._middle_name}, address={self._address}, phone={self._phone})")

    def short_str(self):
        initials = f"{self._first_name[0] if self._first_name else ''}.{self._middle_name[0] if self._middle_name else ''}."
        return f"{self._last_name} {initials}"

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return (super().__eq__(other) and
                self._first_name == other._first_name and
                self._middle_name == other._middle_name and
                self._address == other._address)

    # Перегрузка для сложения (объединение имен)
    def __add__(self, other):
        if not isinstance(other, Client):
            return NotImplemented
        new_last_name = self._last_name + "-" + other._last_name
        new_first_name = self._first_name + " " + other._first_name
        new_middle_name = self._middle_name + " " + other._middle_name
        new_address = self._address + "; " + other._address
        new_phone = self._phone + " / " + other._phone
        return Client(self._client_id, new_last_name, new_first_name, new_middle_name, new_address, new_phone)

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self.validate_name(value)
        self._first_name = value
        # Обновляем initials при изменении first_name
        self._initials = f"{self._first_name[0] if self._first_name else ''}.{self._middle_name[0] if self._middle_name else ''}."

    @property
    def middle_name(self):
        return self._middle_name

    @middle_name.setter
    def middle_name(self, value):
        self.validate_name(value)
        self._middle_name = value
        # Обновляем initials при изменении middle_name
        self._initials = f"{self._first_name[0] if self._first_name else ''}.{self._middle_name[0] if self._middle_name else ''}."

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Адрес должен быть непустой строкой")
        self._address = value


# Код для ввода и вывода (не трогает классы выше)
if __name__ == "__main__":
    print("Добро пожаловать в демонстрацию классов клиентов (с перегрузкой конструкторов)!")

    # Создание Client обычным способом (6 аргументов) - hardcoded
    print("\n1. Создание объекта Client обычным способом (6 аргументов) - hardcoded")
    try:
        client1 = Client("123", "Иванов", "Иван", "Иванович", "Москва", "+7-123-456-78-90")
        print(f"Создан объект: {client1}")
        print(f"Короткая строка: {client1.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Добавлено: Создание Client с вводом полей по отдельности
    print("\n1a. Создание объекта Client с вводом полей по отдельности")
    try:
        client_id = input("Введите client_id: ").strip()
        last_name = input("Введите last_name: ").strip()
        first_name = input("Введите first_name: ").strip()
        middle_name = input("Введите middle_name: ").strip()
        address = input("Введите address: ").strip()
        phone = input("Введите phone: ").strip()
        client1a = Client(client_id, last_name, first_name, middle_name, address, phone)
        print(f"Создан объект: {client1a}")
        print(f"Короткая строка: {client1a.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Создание Client из строки через перегрузку конструктора
    print(
        "\n2. Создание объекта Client из строки через перегрузку (формат: client_id;last_name;first_name;middle_name;address;phone)")
    input_str = input("Введите строку для Client: ")
    try:
        client2 = Client(input_str)  # Перегрузка!
        print(f"Создан объект: {client2}")
        print(f"Короткая строка: {client2.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Создание Client из JSON через перегрузку конструктора
    print(
        "\n3. Создание объекта Client из JSON через перегрузку (формат: {\"client_id\": \"...\", \"last_name\": \"...\", ...})")
    json_str = input("Введите JSON для Client: ")
    try:
        client3 = Client(json_str)  # Перегрузка!
        print(f"Создан объект: {client3}")
        print(f"Короткая строка: {client3.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Создание Client из JSON-файла
    print("\n3a. Создание объекта Client из JSON-файла")
    file_path = input("Введите путь к JSON-файлу для Client: ").strip()
    try:
        client3a = Client.from_json_file(file_path)
        print(f"Создан объект: {client3a}")
        print(f"Короткая строка: {client3a.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Создание ClientShort обычным способом (4 аргумента) - hardcoded
    print("\n4. Создание объекта ClientShort обычным способом (4 аргумента) - hardcoded")
    try:
        client_short1 = ClientShort("456", "Петров", "П.П.", "+7-987-654-32-10")
        print(f"Создан объект: {client_short1}")
        print(f"Короткая строка: {client_short1.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Добавлено: Создание ClientShort с вводом полей по отдельности
    print("\n4a. Создание объекта ClientShort с вводом полей по отдельности")
    try:
        client_id_short = input("Введите client_id для ClientShort: ").strip()
        last_name_short = input("Введите last_name для ClientShort: ").strip()
        initials = input("Введите initials для ClientShort: ").strip()
        phone_short = input("Введите phone для ClientShort: ").strip()
        client_short1a = ClientShort(client_id_short, last_name_short, initials, phone_short)
        print(f"Создан объект: {client_short1a}")
        print(f"Короткая строка: {client_short1a.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Создание ClientShort из строки через перегрузку конструктора
    print("\n5. Создание объекта ClientShort из строки через перегрузку (формат: client_id;last_name;initials;phone)")
    input_str_short = input("Введите строку для ClientShort: ")
    try:
        client_short2 = ClientShort(input_str_short)  # Перегрузка!
        print(f"Создан объект: {client_short2}")
        print(f"Короткая строка: {client_short2.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Создание ClientShort из JSON через перегрузку конструктора
    print(
        "\n6. Создание объекта ClientShort из JSON через перегрузку (формат: {\"client_id\": \"...\", \"last_name\": \"...\", \"initials\": \"...\", \"phone\": \"...\"})")
    json_str_short = input("Введите JSON для ClientShort: ")
    try:
        client_short3 = ClientShort(json_str_short)  # Перегрузка!
        print(f"Создан объект: {client_short3}")
        print(f"Короткая строка: {client_short3.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Создание ClientShort из JSON-файла
    print("\n6a. Создание объекта ClientShort из JSON-файла")
    file_path_short = input("Введите путь к JSON-файлу для ClientShort: ").strip()
    try:
        client_short3a = ClientShort.from_json_file(file_path_short)
        print(f"Создан объект: {client_short3a}")
        print(f"Короткая строка: {client_short3a.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Демонстрация свойств и сеттеров (если объекты созданы успешно)
    if 'client1' in locals():
        print("\n7. Демонстрация свойств и изменения Client1")
        print(f"Текущий client_id: {client1.client_id}")
        new_id = input("Введите новый client_id: ")
        try:
            client1.client_id = new_id
            print(f"Новый client_id: {client1.client_id}")
        except ValueError as e:
            print(f"Ошибка при изменении: {e}")

    # Сравнение объектов (__eq__)
    if 'client1' in locals() and 'client2' in locals():
        print("\n8. Проверка перегрузки __eq__ (сравнение Client1 и Client2)")
        print(f"Client1 == Client2: {client1 == client2}")
        print(f"Client1 != Client2: {client1 != client2}")

    # Проверка перегрузки __lt__ (сравнение по ID)
    if 'client1' in locals() and 'client2' in locals():
        print("\n9. Проверка перегрузки __lt__ (сравнение по client_id)")
        print(f"Client1 < Client2: {client1 < client2}")
        print(f"Client1 > Client2: {client1 > client2}")

    # Проверка перегрузки __str__ (автоматически при печати)
    if 'client1' in locals():
        print("\n10. Проверка перегрузки __str__ (печать объекта)")
        print(f"str(Client1): {str(client1)}")

    # Проверка перегрузки __add__ (сложение клиентов)
    if 'client1' in locals() and 'client2' in locals():
        print("\n11. Проверка перегрузки __add__ (объединение Client1 и Client2)")
        try:
            combined = client1 + client2
            print(f"Объединенный клиент: {combined}")
        except Exception as e:
            print(f"Ошибка при объединении: {e}")

    print("\nДемонстрация завершена!")
