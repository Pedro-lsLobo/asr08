"""
Rodar na máquina CLIENT 1 (172.31.67.45)

Ordem de inicialização:
  1. Inicie server.py  na máquina do servidor   (172.31.64.30)
  2. Inicie run_client2.py na máquina client2   (172.31.75.172)
  3. Inicie este script na máquina client1      (172.31.67.45)
"""
import pickle
from time     import sleep
from constRPC import *
from client   import Client
from dbclient import DBClient

def main():
  # Cria o socket de escuta do client1 (para receber mensagens de volta, se necessário)
  c1 = Client(PORTC1)

  # Cria o stub que aponta para o servidor de listas
  dbC1 = DBClient(HOSTS, PORTS)

  # Cria uma nova lista no servidor e obtém o listID
  listID = dbC1.create()
  print(f"[Client1] Lista criada com ID={listID}")

  # Adiciona dado à lista
  dbC1.appendData('Client 1')
  print(f"[Client1] Appended 'Client 1'")

  # Aguarda um momento para garantir que client2 já está escutando
  print(f"[Client1] Aguardando 3s antes de enviar stub para Client2...")
  sleep(3)

  # Serializa e envia o stub (DBClient) para o client2
  # O stub carrega consigo o host/porta do servidor e o listID — é a referência global
  c1.sendTo(HOSTC2, PORTC2, dbC1)
  print(f"[Client1] Stub (referência global) enviado para Client2 ({HOSTC2}:{PORTC2})")

if __name__ == "__main__":
  main()
