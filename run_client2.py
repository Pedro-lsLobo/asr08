import pickle
from constRPC import *
from client   import Client
from dbclient import DBClient

def main():
  c2 = Client(PORTC2)
  print(f"[Client2] Aguardando stub de Client1 na porta {PORTC2}...")

  data = c2.recvAny()

  dbC2 = pickle.loads(data)
  print(f"[Client2] Stub recebido! listID={dbC2.listID}, apontando para {dbC2.host}:{dbC2.port}")

  dbC2.appendData('Client 2')
  print(f"[Client2] Appended 'Client 2'")

  result = dbC2.getValue()
  print(f"[Client2] Valor da lista: {result}")

  stop_sock = __import__('socket').socket()
  stop_sock.connect((HOSTS, PORTS))
  stop_sock.send(pickle.dumps([STOP]))
  stop_sock.close()
  print("[Client2] Sinal STOP enviado ao servidor.")

if __name__ == "__main__":
  main()
