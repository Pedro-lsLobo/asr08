from client import *
from dbclient import *
from constRPC import *
from time import sleep

if __name__ == "__main__":
    c1 = Client(PORTC1)
    dbC1 = DBClient(HOSTS, PORTS)

    dbC1.create()
    dbC1.appendData('Client 1')

    print("Client1 enviando stub para Client2...")
    sleep(5)  # garantir que client2 já iniciou

    c1.sendTo(HOSTC2, PORTC2, dbC1)