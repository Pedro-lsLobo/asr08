from server import *
from constRPC import *

if __name__ == "__main__":
    s = Server(PORTS)
    print("Servidor rodando...")
    s.run()