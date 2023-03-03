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


class LoginRequestMessage(Message):
    message_type = 0

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {'username': self.username, 'password': self.password}


class LoginResponseMessage(Message):
    message_type = 1

    def __init__(self, success, msg):
        self.success = success
        self.msg = msg

    @classmethod
    def from_dict(cls, data):
        return cls(data['success'], data['msg'])


class ChatAllRequestMessage(Message):
    message_type = 2

    def __init__(self, content, username):
        self.content = content
        self.username = username

    def to_dict(self):
        return {'content': self.content, 'username': self.username}


class ChatAllResponseMessage(Message):
    message_type = 3

    def __init__(self, content, username):
        self.content = content
        self.username = username

    @classmethod
    def from_dict(cls, data):
        return cls(data['content'], data['username'])


class ChatToOneRequestMessage(Message):
    message_type = 4

    def __init__(self, from_user, to_user, content):
        self.from_user = from_user
        self.to_user = to_user
        self.content = content

    def to_dict(self):
        return {'from_user': self.from_user, "to_user": self.to_user, 'content': self.content}


class ChatToOneResponseMessage(Message):
    message_type = 5

    def __init__(self, from_user, to_user, content):
        self.from_user = from_user
        self.to_user = to_user
        self.content = content

    @classmethod
    def from_dict(cls, data):
        return cls(data["from_user"], data["to_user"], data["content"])
