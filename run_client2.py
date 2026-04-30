"""
Rodar na máquina CLIENT 2 (172.31.75.172)

Ordem de inicialização:
  1. Inicie server.py      na máquina do servidor (172.31.64.30)
  2. Inicie este script    na máquina client2     (172.31.75.172)  <- este
  3. Inicie run_client1.py na máquina client1     (172.31.67.45)
"""
import pickle
from constRPC import *
from client   import Client
from dbclient import DBClient

def main():
  # Cria o socket de escuta do client2
  c2 = Client(PORTC2)
  print(f"[Client2] Aguardando stub de Client1 na porta {PORTC2}...")

  # Bloqueia até que client1 envie o stub
  data = c2.recvAny()

  # Desserializa o stub — agora dbC2 é uma referência global para a mesma lista
  dbC2 = pickle.loads(data)
  print(f"[Client2] Stub recebido! listID={dbC2.listID}, apontando para {dbC2.host}:{dbC2.port}")

  # Usa o stub para adicionar dado na mesma lista remota
  dbC2.appendData('Client 2')
  print(f"[Client2] Appended 'Client 2'")

  # Lê o valor atual da lista
  result = dbC2.getValue()
  print(f"[Client2] Valor da lista: {result}")

  # Envia sinal de parada ao servidor
  stop_sock = __import__('socket').socket()
  stop_sock.connect((HOSTS, PORTS))
  stop_sock.send(pickle.dumps([STOP]))
  stop_sock.close()
  print("[Client2] Sinal STOP enviado ao servidor.")

if __name__ == "__main__":
  main()
