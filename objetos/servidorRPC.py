from uuid import UUID, uuid1

from rpyc import Service
from rpyc.utils.server import ThreadedServer


class User:
    def __init__(self, id: UUID, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"


class ChatService(Service):
    exposed_user_list: list[User] = []

    def exposed_enter_room(self, username: str) -> None:
        new_user = User(id=str(uuid1()), name=username)
        ChatService.exposed_user_list.append(new_user)

    def exposed_get_user_list(self) -> list[User]:
        return ChatService.exposed_user_list


job = ThreadedServer(
    ChatService,
    port=18861,
    protocol_config={
        "allow_public_attrs": True,
    },
)

job.start()
