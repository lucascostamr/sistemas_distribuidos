from uuid import UUID, uuid1
from typing import Callable

from rpyc import Service
from rpyc.utils.server import ThreadedServer


class User:
    def __init__(self, id: UUID, name: str, conn):
        self.id = id
        self.name = name
        self.conn = conn

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"


class ChatService(Service):
    exposed_user_dict: dict[str, User] = {}
    exposed_room: list[User] = []

    def __init__(self):
        self._client_name = None

    def on_connect(self, conn):
        self._conn = conn

    def on_disconnect(self, conn):
        print("Fechou")
        for user in ChatService.exposed_room:
            if user.conn == conn:
                return ChatService.exposed_room.remove(user)


    def exposed_register_user(self, username: str) -> None:
        new_user = {
            username: User (
                id=str(uuid1()),
                name=username,
                conn = self._conn
            )
        }

        ChatService.exposed_user_dict.update(new_user)
        # print(ChatService.exposed_user_dict)

    def exposed_enter_room(self, username: str) -> None:
        user = ChatService.exposed_user_dict[username]
        ChatService.exposed_room.append(user)
        # print(ChatService.exposed_room)
        self._notify(f"{username} have just entered the room")
        print("Saiu")

    def exposed_leave_room(self, username: str) -> None:
        del ChatService.exposed_user_dict[username]

    def exposed_get_user_list(self) -> list[User]:
        return list(ChatService.exposed_user_dict.values())

    def exposed_get_room(self) -> list[User]:
        return ChatService.exposed_room

    def _notify(self, message):
        for user in ChatService.exposed_room:
            try:
                user.conn.root.receive_message(message)
                print("OPA")
            except Exception as e:
                print(e)

job = ThreadedServer(
    ChatService,
    port=18861,
    protocol_config={
        'allow_public_attrs': True,
    }
)

job.start()
