from uuid import uuid1
import rpyc

proxy = rpyc.connect('localhost', 18861)

username = input("Digite seu nome: ")

new_user = {
    "id": uuid1(),
    "name": username
}

proxy.root.user_list.append(new_user)

lista = proxy.root.get_user_list()
print(lista)