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
    exposed_user_dict: dict[str, User] = {}
    exposed_room: list[User] = []

    def exposed_register_user(self, username: str) -> None:
        new_user = {
            username: User (
                id=str(uuid1()),
                name=username
            )
        }

        ChatService.exposed_user_dict.update(new_user)

    def exposed_enter_room(self, username: str) -> None:
        user = ChatService.exposed_user_dict[username]
        ChatService.exposed_room.append(user)

    def exposed_get_user_list(self) -> list[User]:
        return list(ChatService.exposed_user_dict.values())

    def exposed_get_room(self) -> list[User]:
        return ChatService.exposed_room


job = ThreadedServer(
    ChatService,
    port=18861
)

job.start()
