import rpyc

proxy = rpyc.connect('localhost', 18861)

username = input("Digite seu nome: ")
proxy.root.register_user(username)
proxy.root.enter_room(username)
lista = proxy.root.get_user_list()
room = proxy.root.get_room()
print(lista)
print(room)