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
