import pickle
from socket   import *
from constRPC import *

class Client:
  def __init__(self, port):
    self.host = ''
    self.port = port
    self.sock = socket()
    self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    self.sock.bind((self.host, self.port))
    self.sock.listen(2)

  def sendTo(self, host, port, data):
    sock = socket()
    sock.connect((host, port))
    sock.send(pickle.dumps(data))
    sock.close()

  def recvAny(self):
    (conn, addr) = self.sock.accept()
    return conn.recv(4096)
