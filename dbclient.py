import pickle
from socket   import *
from constRPC import *

class DBClient:
  def __init__(self, host, port, listID=None):
    self.host   = host     # endereço do servidor de listas
    self.port   = port     # porta do servidor de listas
    self.listID = listID   # ID da lista gerenciada por este stub

  def __sendrecv(self, message):
    sock = socket()
    sock.connect((self.host, self.port))
    sock.send(pickle.dumps(message))
    result = pickle.loads(sock.recv(4096))
    sock.close()
    return result

  def create(self):
    assert self.listID == None
    self.listID = self.__sendrecv([CREATE])
    return self.listID

  def getValue(self):
    assert self.listID != None
    return self.__sendrecv([GETVALUE, self.listID])

  def appendData(self, data):
    assert self.listID != None
    return self.__sendrecv([APPEND, data, self.listID])
