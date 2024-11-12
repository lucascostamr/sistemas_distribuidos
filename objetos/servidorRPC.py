from rpyc.utils.server import ThreadedServer
from rpyc import Service

class ChatService(Service):
    exposed_user_list: list[str] = []

    def exposed_get_user_list(self):
        return ChatService.exposed_user_list

t = ThreadedServer(ChatService, port=18861, protocol_config={
    'allow_public_attrs': True,
})

t.start()
