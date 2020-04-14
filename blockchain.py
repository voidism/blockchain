import pickle
from block import Block
from db import DB

class Blockchain(object):
    """ Blockchain keeps a sequence of Blocks

    Attributes:
        ~~_blocks (Block object): a genesis Blcok.~~
        _tip (bytes): Point to the latest hash of block.
        _db (DB): DB instance
    """
    latest = 'l'
    db_file = 'blockchain.db'
    genesis_coinbase_data = 'The Times 03/Jan/2009 Chancellor on brink of second bailout for banks'

    def __init__(self):
        self._db = DB(Blockchain.db_file)
        # self._blocks = [Block().pow_of_block()]
        if Blockchain.latest in self._db:
            self._tip = self._db.get(Blockchain.latest)
        else:
            self._tip = None
            genesis = Block(Blockchain.genesis_coinbase_data).pow_of_block()
            self.put_block(genesis)

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

