import pickle
from socket   import *
from constRPC import *

class Server:
  def __init__(self, port=PORTS):
    self.host = ''
    self.port = port
    self.sock = socket()
    self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    self.sock.bind((self.host, self.port))
    self.sock.listen(5)
    self.setOfLists = {}
    print(f"[Server] Escutando em porta {self.port}...")

  def run(self):
    while True:
      (conn, addr) = self.sock.accept()
      print(f"[Server] Conexão de {addr}")
      data = conn.recv(4096)
      request = pickle.loads(data)

      if request[0] == CREATE:
        listID = len(self.setOfLists) + 1
        self.setOfLists[listID] = []
        print(f"[Server] CREATE -> listID={listID}")
        conn.send(pickle.dumps(listID))

      elif request[0] == APPEND:
        listID = request[2]
        data   = request[1]
        self.setOfLists[listID].append(data)
        print(f"[Server] APPEND '{data}' -> lista {listID}: {self.setOfLists[listID]}")
        conn.send(pickle.dumps(OK))

      elif request[0] == GETVALUE:
        listID = request[1]
        result = self.setOfLists[listID]
        print(f"[Server] GETVALUE lista {listID}: {result}")
        conn.send(pickle.dumps(result))

      elif request[0] == STOP:
        print("[Server] Recebido STOP. Encerrando.")
        conn.close()
        break

      conn.close()

if __name__ == "__main__":
  server = Server(PORTS)
  server.run()
