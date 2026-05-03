import pickle
from time     import sleep
from constRPC import *
from client   import Client
from dbclient import DBClient

def main():
  c1 = Client(PORTC1)

  dbC1 = DBClient(HOSTS, PORTS)

  listID = dbC1.create()
  print(f"[Client1] Lista criada com ID={listID}")

  dbC1.appendData('Client 1')
  print(f"[Client1] Appended 'Client 1'")

  print(f"[Client1] Aguardando 3s antes de enviar stub para Client2...")
  sleep(3)

  c1.sendTo(HOSTC2, PORTC2, dbC1)
  print(f"[Client1] Stub (referência global) enviado para Client2 ({HOSTC2}:{PORTC2})")

if __name__ == "__main__":
  main()
