from uuid import UUID, uuid1

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
    def __init__(self):
        self._client_name = None
        self.exposed_user_dict: dict[str, User] = {}
        self.exposed_room: list[User] = []

        print("\nChat iniciado!")

    def on_connect(self, conn):
        self._conn = conn

    def on_disconnect(self, conn):
        for user in self.exposed_room:
            if user.conn == conn:
                self.exposed_room.remove(user)
                self._notify(f"{user.name} acabou de deixar a sala.")
                return

    def exposed_register_user(self, username: str) -> None:
        print(f"{username} registrado!")
        new_user = {
            username: User (
                id=str(uuid1()),
                name=username,
                conn = self._conn
            )
        }
        self.exposed_user_dict.update(new_user)

    def exposed_enter_room(self, username: str) -> None:
        user = self.exposed_user_dict[username]
        self.exposed_room.append(user)
        self._notify(f"{username} acabou de entrar na sala.")

    def exposed_leave_room(self, username: str) -> None:
        del self.exposed_user_dict[username]

    def exposed_get_user_list(self) -> list[str]:
        return list(map(lambda user: user.name, self.exposed_user_dict.values()))

    def exposed_send_message(self, username: str, message: str, receiver: str) -> None:
        self._notify(message, username, receiver)

    def _notify(self, message: str, username: str = None, receiver_name: str = "Todos"):
        if receiver_name != "Todos":
            if receiver_name not in self.exposed_user_dict:
                print("Usuario nao encontrado!")
                return

            receiver = self.exposed_user_dict[receiver_name]
            current_user = self.exposed_user_dict[username]

            receiver.conn.root.receive_message(message)
            current_user.conn.root.receive_message(message)
            return

        for user in self.exposed_room:
            try:
                user.conn.root.receive_message(message)
            except Exception as e:
                print(e)

job = ThreadedServer(
    ChatService(),
    port=18861
)

job.start()
