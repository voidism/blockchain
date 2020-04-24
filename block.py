import time
import hashlib
import pickle

import utils
from proof_of_work import Pow


class Block(object):
    """ Represents a new Block object.

    Args:
        data (string): Data to be sent.
        prev_block_hash (string): Hash of the previous Block. 

    Attributes:
        _timestamp (bytes): Creation timestamp of Block.
        _data (bytes): Data to be sent.
        _prev_block_hash (bytes): Hash of the previous Block.
        _hash (bytes): Hash of the current Block.
    """

    def __init__(self, data='Genesis Block', prev_block_hash=''):
        self._timestamp = utils.encode(str(int(time.time())))
        self._data = data
        self._prev_block_hash = utils.encode(prev_block_hash)
        self._hash = None # self._set_hash(self._timestamp, self._data, self._prev_block_hash)
        self._nonce = None

    def __repr__(self):
        return '\n+- Block ---------\n| hash <=== %s\n| time = %s\n| data = %s\n|nonce = %s\n| prev ===> %s\n+-----------------'''%(self.hash, self.timestamp, self.data, self.nonce, self.prev_block_hash)

    def pow_of_block(self):
        # Makes the proof of work of the current Block
        pow = Pow(self)
        nonce, hash = pow.run()
        self._nonce, self._hash = nonce, utils.encode(hash)
        return self                        

    '''def _set_hash(self, timestamp, data, prev_block_hash):
        # SetHash calculates and sets block hash
        hash = utils.sum256(timestamp, data,
                            prev_block_hash)
        return utils.encode(hash)'''

    @property
    def hash(self):
        return utils.decode(self._hash)

    @property
    def data(self):
        return self._data

    @property
    def transactions(self):
        return self._data

    @property
    def prev_block_hash(self):
        return utils.decode(self._prev_block_hash)

    @property
    def timestamp(self):
        return str(self._timestamp)

    @property
    def nonce(self):
        return str(self._nonce)

    def hashTX(self):
        # return a hash of the transactions in the block
        tx_hashs = []

        for tx in self.data:
            tx_hashs.append(tx.ID)

        return utils.sum256(utils.encode(''.join(tx_hashs)))

    def serialize(self):
        return pickle.dumps(self)
