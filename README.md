# asr08
.
# Stubs como Referências Remotas — Exemplo RPC

Este exemplo demonstra o uso de **stubs de cliente como referências globais** em sistemas RPC, conforme descrito nas Notas 4.5 e 4.8 de Tanenbaum & van Steen (2025). Um stub `DBClient` é criado por um cliente, serializado, enviado pela rede para um segundo cliente, e usado lá para operar sobre a mesma lista remota — sem que o segundo cliente precise saber previamente o endereço do servidor ou o ID da lista.

---

## Estrutura do Projeto

```
.
├── constRPC.py       # constantes: códigos de operação, IPs e portas
├── server.py         # servidor de listas (gerencia as listas compartilhadas)
├── client.py         # auxiliar de cliente (envio e recebimento de mensagens)
├── dbclient.py       # stub DBClient (implementação da referência global)
├── run_server.py     # ponto de entrada para a máquina do servidor
├── run_client1.py    # ponto de entrada para a máquina do client 1
└── run_client2.py    # ponto de entrada para a máquina do client 2
```

---

## Como Funciona

1. O **Servidor** inicia e fica aguardando requisições RPC.
2. O **Client 1** cria um stub `DBClient` apontando para o servidor, cria uma lista remota, adiciona `'Client 1'` a ela e então **serializa o stub** (`pickle.dumps`) e o envia via socket para o Client 2.
3. O **Client 2** recebe o stub serializado, desserializa (`pickle.loads`) e passa a ter uma referência completamente funcional para a **mesma lista remota**. Ele adiciona `'Client 2'` e imprime o resultado.

Saída esperada no Client 2:
```
['Client 1', 'Client 2']
```

O ponto central é que o `DBClient` carrega dentro de si o endereço do servidor e o ID da lista. Uma vez serializado e enviado pela rede, ele funciona como uma **referência global** — válida em qualquer processo que tenha acesso à rede do servidor, não apenas no processo que o criou.

---

## Executando na AWS (3 Instâncias EC2)

### Máquinas

| Papel    | IP Privado      | Porta |
|----------|-----------------|-------|
| Server   | 172.31.64.30    | 5678  |
| Client 1 | 172.31.67.45    | 5679  |
| Client 2 | 172.31.75.172   | 5680  |

### Configuração em cada máquina

```bash
git clone <url-do-repositorio>
cd stubs-as-remote-references-Pedro-lsLobo
```

### Ordem de inicialização (importante!)

**Passo 1 — Máquina do servidor:**
```bash
python3 run_server.py
```

**Passo 2 — Máquina do Client 2** (deve estar ouvindo antes do Client 1 enviar o stub):
```bash
python3 run_client2.py
```

**Passo 3 — Máquina do Client 1:**
```bash
python3 run_client1.py
```

O Client 2 precisa ser iniciado antes do Client 1 porque `recvAny()` é uma chamada bloqueante — ele trava esperando uma conexão chegar. Se o Client 1 rodar primeiro, ele tentará conectar no Client 2 antes de qualquer processo estar ouvindo naquela porta, e a conexão será recusada.

---

## Alterações em Relação ao Código Original

O código original (`run.py`) usava `multiprocessing` para rodar tudo em uma única máquina. Para distribuir entre 3 máquinas separadas, as seguintes mudanças foram feitas:

### `constRPC.py`
- Adicionadas as variáveis `HOSTC1` e `HOSTC2` com os IPs privados reais de cada instância EC2.
- `HOSTS` deixou de ser `''` e passou a ser o IP real do servidor `172.31.64.30`.
- Portas alteradas de `50004/50053/50054` para `5678/5679/5680`, adequando ao intervalo liberado nas regras do Security Group das instâncias AWS.

### `client.py`
- `self.host = 'localhost'` foi alterado para `self.host = ''`, fazendo o socket escutar em todas as interfaces de rede, não apenas no loopback. Sem essa mudança, conexões vindas de outras máquinas eram recusadas.
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
- **`run.py`** — mantido no repositório como referência (versão original para uma única máquina), mas não é usado na execução distribuída.
