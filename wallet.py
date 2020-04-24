import os
import hashlib
import binascii

import ecdsa

import utils


class Wallet(object):
    def __init__(self):
        self._private_key = os.urandom(32)
        self._private_key_wif = utils.privkey_to_wif(self._private_key)
        self._public_key = utils.privkey_to_pubkey(self._private_key)
        self._hash_public_key = utils.pubkey2hash(self._public_key)
        self._address = utils.hash2address(self._hash_public_key)

    @property
    def private_key(self):
        return self._private_key

    @property
    def public_key(self):
        return self._public_key

    @property
    def hash_public_key(self):
        return self._hash_public_key

    @property
    def address(self):
        return self._address


if __name__ == '__main__':
    w = Wallet()
    assert w.hash_public_key == utils.address2hash(
        w.address), "Hash of public key is Not Equal!"