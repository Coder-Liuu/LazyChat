import abc


class Message(abc.ABC):
    message_type = None

    def __repr__(self):
        return f"{type(self).__name__}({', '.join([f'{k}={v!r}' for k, v in self.__dict__.items()])})"

    @classmethod
    def get_message_type(cls):
        return cls.message_type

    @classmethod
    def get_message_class(cls, message_type):
        for subclass in cls.__subclasses__():
            if subclass.message_type == message_type:
                return subclass
        raise ValueError(f"No message class for type {message_type}")

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, data):
        pass



class LoginRequestMessage(Message):
    message_type = 0

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {'username': self.username, 'password': self.password}

    @classmethod
    def from_dict(cls, data):
        return cls(data['username'], data['password'])


class LoginResponseMessage(Message):
    message_type = 1

    def __init__(self, success, msg):
        self.success = success
        self.msg = msg

    @classmethod
    def from_dict(cls, data):
        return cls(data['success'], data['msg'])
