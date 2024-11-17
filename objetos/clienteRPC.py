from rpyc import (
    Service,
    connect,
    BgServingThread
)

from time import sleep

class ClientService(Service):
    exposed_public_message_list = []
    exposed_private_message_list = []

    def exposed_receive_message(self, message: str):
        print(message)

class Client():
    def __init__(self):
        self._conn = connect('localhost', 18861, service=ClientService)
        self.bgsrv = BgServingThread(self._conn)
        self._name: str = None
        self._room: str = None

    def register_user(self) -> None:
        self._name = input("Digite seu nome: ")
        self._conn.root.register_user(self._name)

    def enter_room(self) -> None:
        if not self._name:
            print("Please, provide your name first!")
            return
        self._conn.root.enter_room(self._name)

if __name__ == "__main__":
    client = Client()
    client.register_user()
    client.enter_room()
    while True:
        pass