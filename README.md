# Stubs como Referências Remotas - Exemplo RPC

---

## Estrutura do Projeto:

```
constRPC.py       # constantes: códigos de operação, IPs e portas
server.py         # servidor de listas (gerencia as listas compartilhadas)
client.py         # auxiliar de cliente (envio e recebimento de mensagens)
dbclient.py       # stub DBClient (implementação da referência global)
run_client1.py    # ponto de entrada para a máquina do client 1
run_client2.py    # ponto de entrada para a máquina do client 2
```

---

## Funcionamento:

1. O **Servidor** inicia e fica aguardando requisições RPC.
2. O **Client 1** cria um stub `DBClient` apontando para o servidor, cria uma lista remota, adiciona `'Client 1'` a ela e então **serializa o stub** (`pickle.dumps`) e o envia via socket para o Client 2.
3. O **Client 2** recebe o stub serializado, desserializa (`pickle.loads`) e passa a ter uma referência completamente funcional para a **mesma lista remota**. Ele adiciona `'Client 2'` e imprime o resultado.

Saída esperada no Client 2:
```
['Client 1', 'Client 2']
```
---

## Executando na AWS (3 Instâncias EC2)

### Máquinas

| Papel    | IP Público         | Porta |
|----------|--------------------|-------|
| Server   | 44.202.179.145     | 5678  |
| Client 1 | 98.84.55.114       | 5679  |
| Client 2 | 34.205.26.151      | 5680  |

As portas 5678–5680 foram liberadas nas regras de entrada do Security Group de cada instância.

### Ordem de inicialização

**Passo 1 — Máquina do servidor:**
```bash
python3 server.py
```

**Passo 2 — Máquina do Client 2** :
```bash
python3 run_client2.py
```

**Passo 3 — Máquina do Client 1:**
```bash
python3 run_client1.py
```

O Client 2 precisa ser iniciado antes do Client 1 porque `recvAny()` é uma chamada bloqueante.

---

## Alterações em Relação ao Código Original

O código original (`run.py`) usava `multiprocessing` para rodar tudo em uma única máquina. Para distribuir entre 3 máquinas separadas, as seguintes mudanças foram feitas:

### `constRPC.py`
- Adicionadas as variáveis `HOSTC1` e `HOSTC2` com os IPs públicos de cada instância EC2.
- `HOSTS` deixou de ser `''` e passou a ser o IP público do servidor `44.202.179.145`.
- Portas alteradas de `50004/50053/50054` para `5678/5679/5680`.

### `client.py`
- `self.host = 'localhost'` foi alterado para `self.host = ''`, fazendo o socket escutar em todas as interfaces de rede, não apenas no loopback.
- Adicionada a opção `SO_REUSEADDR` para evitar o erro `Address already in use` ao reiniciar.
- Buffer do `recv` aumentado de `1024` para `4096` bytes.

### `server.py`
- `self.host` alterado para `''` pelo mesmo motivo do `client.py`.
- Adicionado `SO_REUSEADDR`.
- Adicionado `conn.close()` após cada requisição para liberar a conexão corretamente.
- Buffer do `recv` aumentado para `4096` bytes.
- Adicionados `print` para acompanhamento da execução.
- Adicionado bloco `if __name__ == "__main__"` para permitir execução direta.

### `dbclient.py`
- Buffer do `recv` aumentado de `1024` para `4096` bytes.

### Arquivos novos
- **`run_client1.py`** — substitui a função `client1()` de `run.py`; inclui um `sleep(3)` para garantir que o Client 2 já está pronto antes de enviar o stub.
- **`run_client2.py`** — substitui a função `client2()` de `run.py`; recebe e usa o stub, depois envia STOP ao servidor.
