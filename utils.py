import hashlib
import ecdsa
import base58
import binascii


def encode(string, code='utf-8'):
    return string.encode(code)


def decode(string, code='utf-8'):
    return string.decode(code)


def sum256(*args):
    m = hashlib.sha256()
    for arg in args:
        m.update(arg)
    return m.hexdigest()

def pubkey2hash(pubkey):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(binascii.unhexlify(pubkey)).digest())
    return ripemd160.digest()

def hash2address(_hash):
    data = b'0' + _hash # version payload + public key
    return decode(base58.b58encode_check(data)) # base58(version payload + public key + checksum)

def address2hash(address):
    return base58.b58decode_check(encode(address))[1:]

def privkey_to_wif(key):
    data = b'0x80' + binascii.hexlify(key)
    return base58.b58encode_check(data)

def privkey_to_pubkey(key):
    sk = ecdsa.SigningKey.from_string(key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()
    return '04' + decode(binascii.hexlify(vk.to_string()))

