from client import *
import pickle
from constRPC import *

if __name__ == "__main__":
    c2 = Client(PORTC2)

    print("Client2 esperando dados...")
    data = c2.recvAny()

    dbC2 = pickle.loads(data)

    dbC2.appendData('Client 2')

    print("Lista final:", dbC2.getValue())

    c2.sendTo(HOSTS, PORTS, [STOP])