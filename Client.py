import json
import re


class ClientShort:
    @staticmethod
    def validate_client_id(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("ID клиента должен быть непустой строкой")
        # Жесткое ограничение: только буквы, цифры и дефисы
        if not re.match(r'^[a-zA-Z0-9\-_]+$', value):
            raise ValueError("ID клиента может содержать только буквы, цифры, дефисы и подчеркивания")

    @staticmethod
    def validate_family_name(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Фамилия должна быть непустой строкой")
        # Жесткое ограничение: только русские буквы, дефисы и пробелы
        if not re.match(r'^[а-яА-ЯёЁ\- ]+$', value):
            raise ValueError("Фамилия может содержать только русские буквы, дефисы и пробелы")

    @staticmethod
    def validate_initials(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Инициалы должны быть непустой строкой")
        # Жесткое ограничение: формат "И.О."
        if not re.match(r'^[а-яА-ЯёЁ]\.\s*[а-яА-ЯёЁ]\.$', value):
            raise ValueError("Инициалы должны быть в формате: И.О. (например: И.И.)")

    @staticmethod
    def validate_phone(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Телефон должен быть непустой строкой")

        # Жесткое ограничение: строгий формат +7-XXX-XXX-XX-XX
        pattern = r'^\+7-\d{3}-\d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, value):
            raise ValueError("Телефон должен быть в формате: +7-XXX-XXX-XX-XX (например: +7-912-345-67-89)")

    def __init__(self, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                # Попытка парсинга как JSON
                try:
                    data = json.loads(arg)
                    client_id = data.get("client_id", "")
                    family_name = data.get("family_name", "")
                    initials = data.get("initials", "")
                    phone = data.get("phone", "")
                except json.JSONDecodeError:
                    # Парсинг как строка: client_id;family_name;initials;phone
                    parts = arg.split(';')
                    if len(parts) != 4:
                        raise ValueError("Неверный формат строки или JSON")
                    client_id = parts[0].strip()
                    family_name = parts[1].strip()
                    initials = parts[2].strip()
                    phone = parts[3].strip()
            elif isinstance(arg, dict):
                # Прямая передача dict (JSON-like)
                client_id = arg.get("client_id", "")
                family_name = arg.get("family_name", "")
                initials = arg.get("initials", "")
                phone = arg.get("phone", "")
            else:
                raise ValueError("Неверный тип аргумента для перегрузки")
        elif len(args) == 4:
            client_id, family_name, initials, phone = args
        else:
            raise ValueError("Неверное количество аргументов для ClientShort")

        # Валидация и инициализация
        self.validate_client_id(client_id)
        self.validate_family_name(family_name)
        self.validate_initials(initials)
        self.validate_phone(phone)
        self._client_id = client_id
        self._family_name = family_name
        self._initials = initials
        self._phone = phone

    @classmethod
    def from_string(cls, s):
        # Парсинг строки в формате: client_id;family_name;initials;phone
        parts = s.split(';')
        if len(parts) != 4:
            raise ValueError("Неверный формат строки")
        client_id = parts[0].strip()
        family_name = parts[1].strip()
        initials = parts[2].strip()
        phone = parts[3].strip()
        return cls(client_id, family_name, initials, phone)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        client_id = data.get("client_id", "")
        family_name = data.get("family_name", "")
        initials = data.get("initials", "")
        phone = data.get("phone", "")
        return cls(client_id, family_name, initials, phone)

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
        return f"ClientShort(client_id={self._client_id}, family_name={self._family_name}, initials={self._initials}, phone={self._phone})"

    def short_str(self):
        return f"{self._family_name} {self._initials} Тел: {self._phone}"

    # Перегрузка для сравнения
    def __eq__(self, other):
        if not isinstance(other, ClientShort):
            return False
        return (self._client_id == other._client_id and
                self._family_name == other._family_name and
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
    def family_name(self):
        return self._family_name

    @family_name.setter
    def family_name(self, value):
        self.validate_family_name(value)
        self._family_name = value

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
    @staticmethod
    def validate_given_name(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя должно быть непустой строкой")
        # Жесткое ограничение: только русские буквы и дефисы
        if not re.match(r'^[а-яА-ЯёЁ\-]+$', value):
            raise ValueError("Имя может содержать только русские буквы и дефисы")

    @staticmethod
    def validate_patronymic(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Отчество должно быть непустой строкой")
        # Жесткое ограничение: только русские буквы и дефисы
        if not re.match(r'^[а-яА-ЯёЁ\-]+$', value):
            raise ValueError("Отчество может содержать только русские буквы и дефисы")

    @staticmethod
    def validate_address(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Адрес должен быть непустой строкой")
        # Жесткое ограничение: русские/английские буквы, цифры, основные знаки препинания
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9\-\s\.,/]+$', value):
            raise ValueError("Адрес может содержать только буквы, цифры, дефисы, точки, запятые и пробелы")

    def __init__(self, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                # Попытка парсинга как JSON
                try:
                    data = json.loads(arg)
                    client_id = data.get("client_id", "")
                    family_name = data.get("family_name", "")
                    given_name = data.get("given_name", "")
                    patronymic = data.get("patronymic", "")
                    address = data.get("address", "")
                    phone = data.get("phone", "")
                    initials = f"{given_name[0] if given_name else ''}.{patronymic[0] if patronymic else ''}."
                except json.JSONDecodeError:
                    # Парсинг как строка: client_id;family_name;given_name;patronymic;address;phone
                    parts = arg.split(';')
                    if len(parts) != 6:
                        raise ValueError("Неверный формат строки или JSON")
                    client_id = parts[0].strip()
                    family_name = parts[1].strip()
                    given_name = parts[2].strip()
                    patronymic = parts[3].strip()
                    address = parts[4].strip()
                    phone = parts[5].strip()
                    initials = f"{given_name[0] if given_name else ''}.{patronymic[0] if patronymic else ''}."
            elif isinstance(arg, dict):
                # Прямая передача dict (JSON-like)
                client_id = arg.get("client_id", "")
                family_name = arg.get("family_name", "")
                given_name = arg.get("given_name", "")
                patronymic = arg.get("patronymic", "")
                address = arg.get("address", "")
                phone = arg.get("phone", "")
                initials = f"{given_name[0] if given_name else ''}.{patronymic[0] if patronymic else ''}."
            else:
                raise ValueError("Неверный тип аргумента для перегрузки")
        elif len(args) == 6:
            client_id, family_name, given_name, patronymic, address, phone = args
            initials = f"{given_name[0] if given_name else ''}.{patronymic[0] if patronymic else ''}."
        else:
            raise ValueError("Неверное количество аргументов для Client")

        # Валидация и инициализация дополнительных полей
        self.validate_family_name(family_name)
        self.validate_given_name(given_name)
        self.validate_patronymic(patronymic)
        self.validate_address(address)
        self.validate_phone(phone)

        # Инициализация родительского класса
        super().__init__(client_id, family_name, initials, phone)
        self._given_name = given_name
        self._patronymic = patronymic
        self._address = address

    @classmethod
    def from_string(cls, s):
        # Парсинг строки в формате: client_id;family_name;given_name;patronymic;address;phone
        parts = s.split(';')
        if len(parts) != 6:
            raise ValueError("Неверный формат строки")
        client_id = parts[0].strip()
        family_name = parts[1].strip()
        given_name = parts[2].strip()
        patronymic = parts[3].strip()
        address = parts[4].strip()
        phone = parts[5].strip()
        return cls(client_id, family_name, given_name, patronymic, address, phone)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        client_id = data.get("client_id", "")
        family_name = data.get("family_name", "")
        given_name = data.get("given_name", "")
        patronymic = data.get("patronymic", "")
        address = data.get("address", "")
        phone = data.get("phone", "")
        return cls(client_id, family_name, given_name, patronymic, address, phone)

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
        return (f"Client(client_id={self._client_id}, family_name={self._family_name}, given_name={self._given_name}, "
                f"patronymic={self._patronymic}, address={self._address}, phone={self._phone})")

    def short_str(self):
        return f"{self._family_name} {self._given_name[0] if self._given_name else ''}.{self._patronymic[0] if self._patronymic else ''}."

    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return (super().__eq__(other) and
                self._given_name == other._given_name and
                self._patronymic == other._patronymic and
                self._address == other._address)

    # Перегрузка для сложения (объединение имен)
    def __add__(self, other):
        if not isinstance(other, Client):
            return NotImplemented
        new_family_name = self._family_name + "-" + other._family_name
        new_given_name = self._given_name + " " + other._given_name
        new_patronymic = self._patronymic + " " + other._patronymic
        new_address = self._address + "; " + other._address
        new_phone = self._phone + " / " + other._phone
        return Client(self._client_id, new_family_name, new_given_name, new_patronymic, new_address, new_phone)

    @property
    def given_name(self):
        return self._given_name

    @given_name.setter
    def given_name(self, value):
        self.validate_given_name(value)
        self._given_name = value
        # Обновляем initials при изменении given_name
        self._initials = f"{self._given_name[0] if self._given_name else ''}.{self._patronymic[0] if self._patronymic else ''}."

    @property
    def patronymic(self):
        return self._patronymic

    @patronymic.setter
    def patronymic(self, value):
        self.validate_patronymic(value)
        self._patronymic = value
        # Обновляем initials при изменении patronymic
        self._initials = f"{self._given_name[0] if self._given_name else ''}.{self._patronymic[0] if self._patronymic else ''}."

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self.validate_address(value)
        self._address = value


# Код для ввода и вывода (не трогает классы выше)
if __name__ == "__main__":
    print("Добро пожаловать в демонстрацию классов клиентов (с перегрузкой конструкторов)!")
    print("ОГРАНИЧЕНИЯ ВВОДА:")
    print("- ID клиента: только буквы, цифры, дефисы и подчеркивания")
    print("- ФИО: только русские буквы и дефисы")
    print("- Инициалы: строго в формате 'И.О.'")
    print("- Телефон: строго в формате +7-XXX-XXX-XX-XX")
    print("- Адрес: буквы, цифры, дефисы, точки, запятые и пробелы")

    # Создание Client обычным способом (6 аргументов) - hardcoded
    print("\n1. Создание объекта Client обычным способом (6 аргументов) - hardcoded")
    try:
        client1 = Client("123", "Иванов", "Иван", "Иванович", "Москва, ул. Ленина, д. 1", "+7-123-456-78-90")
        print(f"Создан объект: {client1}")
        print(f"Короткая строка: {client1.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Добавлено: Создание Client с вводом полей по отдельности
    print("\n1a. Создание объекта Client с вводом полей по отдельности")
    try:
        client_id = input("Введите ID клиента: ").strip()
        family_name = input("Введите фамилию: ").strip()
        given_name = input("Введите имя: ").strip()
        patronymic = input("Введите отчество: ").strip()
        address = input("Введите адрес: ").strip()
        phone = input("Введите телефон: ").strip()
        client1a = Client(client_id, family_name, given_name, patronymic, address, phone)
        print(f"Создан объект: {client1a}")
        print(f"Короткая строка: {client1a.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Создание Client из строки через перегрузку конструктора
    print(
        "\n2. Создание объекта Client из строки через перегрузку (формат: client_id;family_name;given_name;patronymic;address;phone)")
    input_str = input("Введите строку для Client: ")
    try:
        client2 = Client(input_str)  # Перегрузка!
        print(f"Создан объект: {client2}")
        print(f"Короткая строка: {client2.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Создание Client из JSON через перегрузку конструктора
    print(
        "\n3. Создание объекта Client из JSON через перегрузку (формат: {\"client_id\": \"...\", \"family_name\": \"...\", ...})")
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
        client_id_short = input("Введите ID клиента для ClientShort: ").strip()
        family_name_short = input("Введите фамилию для ClientShort: ").strip()
        initials = input("Введите инициалы (формат И.О.): ").strip()
        phone_short = input("Введите телефон для ClientShort: ").strip()
        client_short1a = ClientShort(client_id_short, family_name_short, initials, phone_short)
        print(f"Создан объект: {client_short1a}")
        print(f"Короткая строка: {client_short1a.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Создание ClientShort из строки через перегрузку конструктора
    print("\n5. Создание объекта ClientShort из строки через перегрузку (формат: client_id;family_name;initials;phone)")
    input_str_short = input("Введите строку для ClientShort: ")
    try:
        client_short2 = ClientShort(input_str_short)  # Перегрузка!
        print(f"Создан объект: {client_short2}")
        print(f"Короткая строка: {client_short2.short_str()}")
    except ValueError as e:
        print(f"Ошибка: {e}")

    # Создание ClientShort из JSON через перегрузку конструктора
    print(
        "\n6. Создание объекта ClientShort из JSON через перегрузку (формат: {\"client_id\": \"...\", \"family_name\": \"...\", \"initials\": \"...\", \"phone\": \"...\"})")
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
        print(f"Текущий ID клиента: {client1.client_id}")
        new_id = input("Введите новый ID клиента: ")
        try:
            client1.client_id = new_id
            print(f"Новый ID клиента: {client1.client_id}")
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
