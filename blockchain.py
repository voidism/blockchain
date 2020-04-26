import pickle
from collections import defaultdict
from block import Block
from db import DB
from transaction import Transaction
import sys

class ContinueIt(Exception):
    pass

class Blockchain(object):
    latest = 'l'
    db_file = 'blockchain.db'
    genesis_coinbase_data = 'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks'

    def __init__(self, address=None):
        self._db = DB(Blockchain.db_file)
        # self._blocks = [Block().pow_of_block()]
        if Blockchain.latest in self._db:
            self._tip = self._db.get(Blockchain.latest)
            if address is not None:
                print(f'Blockchain already exists in `{Blockchain.db_file}`.\nDelete it first or we cannot build another in the same directory.')
        else:
            self._tip = None
            if address is None:
                print('Initialize Blockchain with no address. Abort!')
                sys.exit(0)
            base_tx = Transaction(to_addr=address, data=Blockchain.genesis_coinbase_data, coinbase=True).set_id()
            genesis = Block([base_tx]).pow_of_block()
            self.put_block(genesis)
            print(f'Create Blockchain; Reward sent to {address}')

    def put_block(self, block):
        # AddBlock saves provided data as a block in the blockchain
        # prev_block_hash = self._blocks[-1].hash
        # self._blocks.append(Block(data, prev_block_hash).pow_of_block())

        self._db.put(block.hash, block.serialize())
        self._db.put('l', block.hash)
        self._tip = block.hash
        self._db.commit()

    def mine_block(self, data):
        new_block = Block(data, self._tip).pow_of_block()
        self.put_block(new_block)

    @property
    def blocks(self):
        # return self._blocks
        current_tip = self._tip
        while current_tip is not None:
            if not current_tip:
                # Encounter genesis block
                raise StopIteration
            encoded_block = self._db.get(current_tip)
            block = pickle.loads(encoded_block)
            yield block
            current_tip = block.prev_block_hash

    def find_utxo(self, pubkey_hash=None):
        # Finds and returns all unspent transaction outputs
        utxos = []
        unspent_txs = self.find_unspent_transactions(pubkey_hash)

        for tx in unspent_txs:
            for out in tx.vout:
                if out.check_key(pubkey_hash):
                    utxos.append(out)

        return utxos

    def find_unspent_transactions(self, pubkey_hash):
        # Returns a list of transactions containing unspent outputs
        spent_txo = defaultdict(list)
        unspent_txs = []
        for block in self.blocks:
            for tx in block.transactions:

                if not tx.coinbase:
                    for vin in tx.vin:
                        if vin.check_key(pubkey_hash):
                            tx_id = vin.tx_id
                            spent_txo[tx_id].append(vin.value)

                tx_id = tx.ID
                try:
                    for out_idx, out in enumerate(tx.vout):
                        # Was the output spent?
                        if spent_txo[tx_id]: # some of the outputs already been spent
                            for spent_out in spent_txo[tx_id]:
                                if spent_out == out_idx:
                                    raise ContinueIt

                        if out.check_key(pubkey_hash):
                            unspent_txs.append(tx)
                except ContinueIt:
                    pass

        return unspent_txs

    def accum_spendable_outputs(self, pubkey_hash, amount):
        # Finds and returns unspent outputs to reference in inputs
        accumulated = 0
        unspent_outputs = defaultdict(list)
        unspent_txs = self.find_unspent_transactions(pubkey_hash)

        for tx in unspent_txs:
            tx_id = tx.ID

            for out_idx, out in enumerate(tx.vout):
                if out.check_key(pubkey_hash):
                    accumulated += out.value
                    unspent_outputs[tx_id].append(out_idx)

                if accumulated >= amount:
                    break
            if accumulated >= amount:
                break

        return accumulated, unspent_outputs

    def find_tx(self, ID):
        for block in self.blocks:
            for tx in block.transactions:
                if tx.ID == ID:
                    return tx
        return None

    def sign_transaction(self, tx, priv_key):
        prev_txs = {}
        for vin in tx.vin:
            prev_tx = self.find_transaction(vin.tx_id)
            prev_txs[prev_tx.ID] = prev_tx
        tx.sign(priv_key, prev_txs)
