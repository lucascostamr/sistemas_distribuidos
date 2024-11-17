from rpyc import (
    Service,
    connect,
    BgServingThread
)

class ClientService(Service):
    def exposed_receive_message(self, message: str):
        print("\n" + message)

class Client():
    def __init__(self):
        self._conn = connect('localhost', 18861, service=ClientService())
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
    
    def send_message(self) -> None:
        message = f"{self._name}: {input("Digite a menssagem: ")}"
        receiver = input("Digite o nome do destinatario: ")
        self._conn.root.send_message(self._name, message, receiver)

    def list_users(self) -> None:
        print(f"Usuarios na sala:\n{self._conn.root.get_user_list()}")

    def leave_room(self) -> None:
        self._conn.root.leave_room(self._name)

if __name__ == "__main__":
    client = Client()
    client.register_user()
    client.enter_room()

    actions = {
        "1": client.send_message,
        "2": client.list_users,
        "3": client.leave_room
    }

    while True:
        print("\nEcolha uma das opcoes abaixo: ")
        action: str = input("\n1 - Enviar mensagem\n2 - Listar usuarios\n3 - Sair da Sala\n\n")
        actions[action]()
        if action == "3":
            break