import json
import os
from typing import List

from block import Block, create_block, create_block_from_dict, create_genesis_block
from network import broadcast_block, broadcast_transaction, list_peers, request_chain


def load_chain(fpath: str) -> List[Block]:
    if os.path.exists(fpath):
        with open(fpath) as f:
            data = json.load(f)
            blockchain = []
            for block_data in data:
                block = create_block_from_dict(block_data)
                blockchain.append(block)
            return blockchain

    return [create_genesis_block()]


def save_chain(fpath: str, chain: list[Block]):
    blockchain_serializable = []
    for b in chain:
        blockchain_serializable.append(b.as_dict())

    with open(fpath, "w") as f:
        json.dump(blockchain_serializable, f, indent=2)


def valid_chain(chain):
    for i in range(1, len(chain)):
        prev_hash = chain[i - 1]["hash"] if isinstance(chain[i - 1], dict) else chain[i - 1].hash
        curr_prev_hash = chain[i]["prev_hash"] if isinstance(chain[i], dict) else chain[i].prev_hash
        if curr_prev_hash != prev_hash:
            return False
    return True


def print_chain(blockchain: List[Block]):
    for b in blockchain:
        print(f"Index: {b.index}, Hash: {b.hash[:10]}..., Tx: {len(b.transactions)}")


def mine_block(
    transactions: List,
    blockchain: List[Block],
    node_id: str,
    reward: int,
    difficulty: int,
    blockchain_fpath: str,
    peers_fpath: str,
    port: int,
):
    # Limitar a 10 transações por bloco (além da coinbase)
    tx_to_include = transactions[:10]
    new_block = create_block(
        tx_to_include,
        blockchain[-1].hash,
        miner=node_id,
        index=len(blockchain),
        reward=reward,
        difficulty=difficulty,
    )
    blockchain.append(new_block)
    # Remover apenas as transações incluídas
    del transactions[:len(tx_to_include)]
    save_chain(blockchain_fpath, blockchain)
    broadcast_block(new_block, peers_fpath, port)
    print(f"[✓] Block {new_block.index} mined and broadcasted.")


def make_transaction(sender, recipient, amount, transactions, peers_file, port):
    tx = {"from": sender, "to": recipient, "amount": amount}
    transactions.append(tx)
    broadcast_transaction(tx, peers_file, port)
    print("[+] Transaction added.")


def get_balance(node_id: str, blockchain: List[Block]) -> float:
    balance = 0
    for block in blockchain:
        for tx in block.transactions:
            if tx["to"] == node_id:
                balance += float(tx["amount"])
            if tx["from"] == node_id:
                balance -= float(tx["amount"])
    return balance


def on_valid_block_callback(fpath, chain):
    save_chain(fpath, chain)


def replace_chain_with_longest(blockchain: list, blockchain_fpath: str, difficulty: int):
    """Verifica as cadeias dos peers e substitui a local pela mais longa válida, se necessário."""
    peers = list_peers('configs/peers.txt')
    longest_chain = [b for b in blockchain]
    for peer in peers:
        peer_chain_data = request_chain(peer, 5002)  # Porta padrão
        if peer_chain_data and len(peer_chain_data) > len(longest_chain):
            # Validar a cadeia recebida
            if valid_chain(peer_chain_data) and all(
                b['hash'].startswith('0' * difficulty) for b in peer_chain_data[1:]
            ):
                print(f"[SYNC] Cadeia mais longa encontrada em {peer}. Substituindo a cadeia local.")
                longest_chain = [create_block_from_dict(b) for b in peer_chain_data]
    if len(longest_chain) > len(blockchain):
        blockchain.clear()
        blockchain.extend(longest_chain)
        save_chain(blockchain_fpath, blockchain)
        print("[SYNC] Cadeia local substituída pela mais longa.")
    else:
        print("[SYNC] Nenhuma cadeia mais longa válida encontrada.")