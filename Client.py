import json
class Client:
    def validate_client_id(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("client_id должен быть непустой строкой")

    @staticmethod
    def validate_name(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя/Фамилия должны быть непустой строкой")

    @staticmethod
    def validate_phone(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Телефон должен быть непустой строкой")

    def _validate_all(self, client_id, last_name, first_name,middle_name, phone):
        self.validate_client_id(client_id)
        self.validate_name(last_name)
        self.validate_name(first_name)
        self.validate_name(middle_name)
        self.validate_phone(phone)

    def __init__(self, client_id: str, last_name: str, first_name: str, middle_name: str, address: str, phone: str):
        self._validate_all(client_id, last_name, first_name,middle_name, phone)
        self._client_id = client_id
        self._last_name = last_name
        self._first_name = first_name
        self._middle_name = middle_name
        self._address = address
        self._phone = phone

        def from_string(cls, s):
            parts = s.split(';')
            if len(parts) != 6:
                raise ValueError("Неверный формат строки")
            return cls(parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[4].strip(),
                       parts[5].strip())

        @classmethod
        def from_json(cls, json_str):
            data = json.loads(json_str)
            return cls(
                data.get("client_id", ""),
                data.get("last_name", ""),
                data.get("first_name", ""),
                data.get("middle_name", ""),
                data.get("address", ""),
                data.get("phone", "")
            )

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
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self.validate_name(value)
        self._first_name = value

    @property
    def middle_name(self):
        return self._middle_name

    @middle_name.setter
    def middle_name(self, value):
        self.validate_middle_name(value)
        self._middle_name = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self.validate_address(value)
        self._address = value

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self.validate_phone(value)
        self._phone = value
