import pickle
import os

class DB():
    def __init__(self, db_file):
        self._db_file = db_file
        if os.path.exists(db_file):
            self._db = pickle.load(open(db_file, 'rb'))
        else:
            self._db = {}

    def get(self, key):
        return self._db[key]

    def put(self, key, value):
        self._db[key] = value

    def delete(self, key):
        del self._db[key]

    def commit(self):
        with open(self._db_file, 'wb') as f:
            pickle.dump(self._db, f)

    def __contains__(self, key):
        return key in self._db

class WalletDB():
    wallet_file = 'wallet.db'
    def __init__(self):
        try:
            with open(WalletDB.wallet_file, 'rb') as f:
                self.wallets = pickle.load(f)
        except FileNotFoundError:
            self.wallets = {}

    def add_wallet(self, addr, wallet):
        self.wallets[addr] = wallet

    def get_addresses(self):
        return [addr for addr in self.wallets.keys()]

    def get_wallet(self, addr):
        return self.wallets[addr]

    def save_to_file(self):
        with open(self.wallet_file, 'wb') as f:
            pickle.dump(self.wallets, f)
