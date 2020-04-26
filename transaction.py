import sys
import pickle
import utils

class Transaction(object):
    subsidy = 2048
    def __init__(self, from_addr=None, to_addr=None, amount=None, chain=None, data=None, walletdb=None, coinbase=False):
        self._id = None
        self._vin = None
        self._vout = None
        self.coinbase = coinbase
        if coinbase:
            if not data:
                data = 'Reward to {0}'.format(to_addr)
            self._vin = [TXInput('', -1, None, data)]
            self._vout = [TXOutput(Transaction.subsidy, to_addr)]
        else:
            assert from_addr is not None and \
                     to_addr is not None and \
                      amount is not None and \
                       chain is not None and \
                    walletdb is not None
            wallet = walletdb.get_wallet(from_addr)
            pubkey_hash = utils.pubkey2hash(wallet.public_key)
            acc, valid_outputs = chain.accum_spendable_outputs(pubkey_hash, amount)
            if acc < amount:
                raise ValueError(f"spendable value: {acc} < amount: {amount}, Abort!")
                sys.exit()

            # Build a list of inputs
            self._vin = []
            for tx_id, outs in valid_outputs.items():
                for out_value in outs:
                    self._vin.append(TXInput(tx_id, out_value, None, wallet.public_key))

            # Build outputs
            self._vout = []
            self._vout.append(TXOutput(amount, to_addr))
            self._vout.append(TXOutput(acc - amount, from_addr))

    def __repr__(self):
        if self.coinbase:
            return '\nCoinbaseTx(\n\tid={0!r},\n\tvin={1!r},\n\tvout={2!r}\n)\n'.format(
            self._id, self._vin, self._vout)
        else:
            return '\nUTXOTx(\n\tid={0!r},\n\tvin={1!r},\n\tvout={2!r}\n)\n'.format(
            self._id, self._vin, self._vout)

    @property
    def ID(self):
        return self._id

    @property
    def vin(self):
        return self._vin

    @property
    def vout(self):
        return self._vout

    def set_id(self):
        # sets ID of a transaction
        self._id = utils.sum256(pickle.dumps(self))
        return self

    def _trimmed_copy(self):
        inputs = []
        outputs = []

        for vin in self.vin:
            inputs.append(TXInput(vin.tx_id, vin.vout, None, None))

        for vout in self.vout:
            outputs.append(TXOutput(vout.value, vout.public_key_hash))

        return Transaction(self.ID, inputs, outputs)
    
    def sign(self, priv_key, prev_txs):
        for vin in self.vin:
            if not prev_txs[vin.tx_id].ID:
                print("Previous transaction is not correct")

        tx_copy = self._trimmed_copy()

        for in_id, vin in enumerate(tx_copy.vin):
            prev_tx = prev_txs[vin.tx_id]
            tx_copy.vin[in_id].signature = None
            tx_copy.vin[in_id].public_key = prev_tx.out[vin.vout].public_key_hash
            tx_copy.ID = tx_copy.hash()
            tx_copy.vin[in_id].public_key = None

            sk = ecdsa.SigningKey.from_string(
                priv_key.hex(), curve=ecdsa.SECP256k1)
            sig = sk.sign(tx_copy.ID)

            self.vin[in_id].signature = sig

    def verify(self, prev_txs):
        for vin in self.vin:
            if not prev_txs[vin.tx_id].ID:
                self.log.error("Previous transaction is not correct")

        tx_copy = self._trimmed_copy()

        for in_id, vin in enumerate(tx_copy.vin):
            prev_tx = prev_txs[vin.tx_id]
            tx_copy.vin[in_id].signature = None
            tx_copy.vin[in_id].public_key = prev_tx.out[vin.vout].public_key_hash
            tx_copy.ID = tx_copy.hash()
            tx_copy.vin[in_id].public_key = None

            sig = self.vin[in_id].signature
            vk = ecdsa.VerifyingKey.from_string(
                vin.public_key[2:].decode('hex'), curve=ecdsa.SECP256k1)
            if not vk.verify(sig, tx_copy.ID):
                return False

        return True


class TXInput(object):
    def __init__(self, txid, value, sig, pubkey):
        self._tx_id = utils.encode(txid)
        self._value = value
        self._script_sig = sig
        self._public_key = pubkey
        self._pubkey_hash = None
        

    def __repr__(self):
        return 'TXInput(tx_id={0!r}, value={1!r}, script_sig={2!r}, public_key={3!r})'.format(
            self._tx_id, self._value, self._script_sig, self._public_key)

    def check_key(self, pubkey_hash):
        # checks whether the address initiated the transaction
        if self._pubkey_hash is None:
            self._pubkey_hash = utils.pubkey2hash(self._public_key)
        return self._pubkey_hash == pubkey_hash

    @property
    def tx_id(self):
        return utils.decode(self._tx_id)

    @property
    def value(self):
        return self._value

class TXOutput(object):
    def __init__(self, value, address):
        self._value = value
        self._pubkey_hash = utils.address2hash(address)

    def __repr__(self):
        return 'TXOutput(value={0!r}, pubkey_hash={1!r})'.format(
            self._value, self._pubkey_hash)

    def check_key(self, pubkey_hash):
        # checks whether the address initiated the transaction
        return self._pubkey_hash == pubkey_hash

    @property
    def value(self):
        return self._value