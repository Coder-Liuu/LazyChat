import abc

class MessageTypes:
    LOGIN_REQUEST = 0
    LOGIN_RESPONSE = 1
    CHAT_ALL_REQUEST = 2
    CHAT_ALL_RESPONSE = 3
    CHAT_TO_ONE_REQUEST = 4
    CHAT_TO_ONE_RESPONSE = 5
    NOTICE_REQUEST = 6
    NOTICE_RESPONSE = 7

    # notice_type
    #    1: 请求好友
    #    2: 同意请求
    #    3: 拒绝请求
    #    10: 返回好友列表
    NOTICE_FRIEND_REQ = 1
    NOTICE_FRIEND_AGREE = 2
    NOTICE_FRIEND_REFUSE = 3
    NOTICE_FRIEND_REMOVE = 4;
    NOTICE_FRIEND_LIST = 10
     # 20: 用户上线通知
     # 21: 用户下线通知
    NOTICE_ONLINE = 20
    NOTICE_OFFLINE = 21


class Message(abc.ABC):
    message_type = 0

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
    message_type = MessageTypes.LOGIN_REQUEST

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def to_dict(self):
        return {'username': self.username, 'password': self.password}


class LoginResponseMessage(Message):
    message_type = MessageTypes.LOGIN_RESPONSE

    def __init__(self, success, msg):
        self.success = success
        self.msg = msg

    @classmethod
    def from_dict(cls, data):
        return cls(data['success'], data['msg'])


class ChatAllRequestMessage(Message):
    message_type = MessageTypes.CHAT_ALL_REQUEST

    def __init__(self, content, username):
        self.content = content
        self.username = username

    def to_dict(self):
        return {'content': self.content, 'username': self.username}


class ChatAllResponseMessage(Message):
    message_type = MessageTypes.CHAT_ALL_RESPONSE

    def __init__(self, content, username):
        self.content = content
        self.username = username

    @classmethod
    def from_dict(cls, data):
        return cls(data['content'], data['username'])


class ChatToOneRequestMessage(Message):
    message_type = MessageTypes.CHAT_ALL_RESPONSE

    def __init__(self, from_user, to_user, content):
        self.from_user = from_user
        self.to_user = to_user
        self.content = content

    def to_dict(self):
        return {'from_user': self.from_user, "to_user": self.to_user, 'content': self.content}


class ChatToOneResponseMessage(Message):
    message_type = MessageTypes.CHAT_TO_ONE_REQUEST

    def __init__(self, from_user, to_user, content):
        self.from_user = from_user
        self.to_user = to_user
        self.content = content

    @classmethod
    def from_dict(cls, data):
        return cls(data["from_user"], data["to_user"], data["content"])


class NoticeRequestMessage(Message):
    message_type = MessageTypes.NOTICE_REQUEST

    # 添加好友、创建群聊、群聊邀请
    def __init__(self, notice_type, from_user, to_user):
        self.notice_type = notice_type
        self.from_user = from_user
        self.to_user = to_user

    def to_dict(self):
        return {'notice_type': self.notice_type, "from_user": self.from_user, "to_user": self.to_user}


class NoticeResponseMessage(Message):
    message_type = MessageTypes.NOTICE_RESPONSE

    # notice_type
    #    1: 请求好友
    #    2: 同意请求
    #    3: 拒绝请求
    #    10: 返回好友列表
    def __init__(self, notice_type, from_user, to_user, reason):
        self.notice_type = notice_type
        self.from_user = from_user
        self.to_user = to_user
        self.reason = reason

    @classmethod
    def from_dict(cls, data):
        return cls(data["notice_type"], data["from_user"], data["to_user"], data["reason"])
