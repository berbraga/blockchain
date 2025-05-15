# Relatório do Trabalho de Blockchain P2P

## 1. Verificação Inicial: Estado Inconsistente

Antes da correção, ao minerar blocos simultaneamente em dois nós, ambos podem apresentar blocos com o mesmo índice, gerando um fork.

**Exemplo de saída:**

**Computador 1:**
```
Index: 0, Hash: 0...,          Tx: 0
Index: 1, Hash: 000024f3c0..., Tx: 1
Index: 2, Hash: 000087593f..., Tx: 1
Index: 3, Hash: 0000b110ba..., Tx: 2
```
**Computador 2:**
```
Index: 0, Hash: 0...,          Tx: 0
Index: 1, Hash: 000024f3c0..., Tx: 1
Index: 2, Hash: 000087593f..., Tx: 1
Index: 3, Hash: 0000b110ba..., Tx: 2
Index: 3, Hash: 0000f190c7..., Tx: 2
```
*Prints reais podem ser capturados durante o teste prático.*

---

## 2. Causa do Erro

O erro ocorre porque, ao minerar simultaneamente, dois nós podem criar blocos com o mesmo índice e `prev_hash`, mas com hashes diferentes. Como não há lógica de consenso, ambos os blocos são aceitos localmente, causando divergência (fork).

---

## 3. Métodos para Resolver Forks

- **Regra da cadeia mais longa (Longest Chain Rule):** Cada nó adota a cadeia mais longa válida.
- **Algoritmos de consenso (ex: Proof of Stake, PBFT):** Mais complexos, usados em blockchains públicas.
- **Ordem por timestamp/prioridade:** Menos comum, pode causar centralização.

---

## 4. Método Selecionado e Implementação

**Selecionado:**  
Regra da cadeia mais longa (Longest Chain Rule).

**Implementação:**  
- Ao detectar um fork, o nó requisita a blockchain dos peers.
- Se encontrar uma cadeia mais longa e válida, substitui a sua.
- Implementado nos arquivos `network.py` e `chain.py`.

---

## 5. Novos Resultados

Após a implementação, ao ocorrer um fork, o nó que detectar a inconsistência irá sincronizar automaticamente com a cadeia mais longa, eliminando blocos duplicados de mesmo índice.

**Exemplo de saída após sincronização:**
```
Index: 0, Hash: 0...,          Tx: 0
Index: 1, Hash: 000024f3c0..., Tx: 1
Index: 2, Hash: 000087593f..., Tx: 1
Index: 3, Hash: 0000b110ba..., Tx: 2
Index: 4, Hash: 0000c1d2e3..., Tx: 1
```
*Inclua prints reais do terminal após o teste prático.*

---

## 6. Arquitetura de Sistema e Software

### Diagrama de Arquitetura de Sistema

```
+-------------------+         +-------------------+
|   Computador 1    | <-----> |   Computador 2    |
|  (nó blockchain)  |         |  (nó blockchain)  |
+-------------------+         +-------------------+
         ^                             ^
         |                             |
         +-----------VPN---------------+
```
- Comunicação P2P via sockets TCP.
- Rede privada via ZeroTier.

### Diagrama de Arquitetura de Software (Simplificado)

```
+-------------------+
|      main.py      |
+-------------------+
         |
         v
+-------------------+
|     chain.py      |<-------------------+
+-------------------+                    |
         |                               |
         v                               |
+-------------------+         +-------------------+
|     block.py      |         |   network.py      |
+-------------------+         +-------------------+
```
- `main.py`: Interface CLI e orquestração.
- `chain.py`: Lógica da blockchain.
- `block.py`: Estrutura e mineração de blocos.
- `network.py`: Comunicação P2P.

---

## Próximos Passos

- Capturar prints reais dos testes para anexar ao relatório.
- Gerar os diagramas em ferramenta visual (ex: draw.io, Lucidchart) e exportar como imagem para o PDF.
- Finalizar o relatório em PDF, incluindo links do GitHub e vídeo de apresentação.

---

**Links:**
- [Repositório no GitHub](https://github.com/SEU_USUARIO/SEU_REPOSITORIO)
- [Vídeo de apresentação](https://youtube.com/SEU_VIDEO) 