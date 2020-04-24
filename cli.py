import argparse

from blockchain import Blockchain
from proof_of_work import Pow
from db import WalletDB
from wallet import Wallet
from transaction import Transaction
import utils

def get_parser():
    parser = argparse.ArgumentParser()
    # A createblockchain command
    parser.add_argument(
        '--create', type=str, help='ADDRESS of create blockchain')
    sub_parser = parser.add_subparsers(help='commands')
    # A print command
    print_parser = sub_parser.add_parser(
        'printchain', help='Print all the blocks of the blockchain')
    print_parser.add_argument('-print', dest='printchain', action='store_true')
    # A print block command
    printblock_parser = sub_parser.add_parser(
        'printblock', help='Print the blocks of the blockchain to height')
    printblock_parser.add_argument('-printblock', dest='printblock', action='store_true')
    printblock_parser.add_argument('-height', dest='height', type=int)
    # A add block command
    addblock_parser = sub_parser.add_parser(
        'addblock', help='Add blocks to the blockchain')
    addblock_parser.add_argument('-addblock', dest='addblock', action='store_true')
    addblock_parser.add_argument('-transaction', dest='transaction', type=str)
        # A createwallet command
    bc_parser = sub_parser.add_parser(
        'createwallet', help='Create a wallet')
    bc_parser.add_argument(
        '-wallet', type=str, dest='wallet', help='WALLET')
    # A getbalance command
    balance_parser = sub_parser.add_parser(
        'getbalance', help='Get balance of ADDRESS')
    balance_parser.add_argument(
        '-address', type=str, dest='balance_address', help='ADDRESS of balance')
    # A send command
    send_parser = sub_parser.add_parser(
        'send', help='Send AMOUNT of coins from FROM address to TO')
    send_parser.add_argument(
        '-from', type=str, dest='send_from', help='FROM')
    send_parser.add_argument(
        '-to', type=str, dest='send_to', help='TO')
    send_parser.add_argument(
        '-amount', type=int, dest='send_amount', help='AMOUNT')

    return parser

def create_blockchain(address):
    bc = Blockchain(address)
    print(f'Create Blockchain; Reward sent to {address}')
    return bc

def print_blockchain(bc=None, lim=None):
    i = 1
    for block in bc.blocks:
        #print("Prev. hash: {0}".format(block.prev_block_hash))
        #print("Hash: {0}".format(block.hash))
        print(block)
        pow = Pow(block)
        print("PoW: {0}".format(pow.validate()))
        if lim is not None:
            if i == lim:
                break
        i += 1

def create_wallet(wallets):
    wallet = Wallet()
    address = wallet.address
    wallets.add_wallet(address, wallet)
    wallets.save_to_file()
    print(f"New address: {address}")

def send(bc, wdb, from_addr, to_addr, amount):
    tx = Transaction(from_addr, to_addr, amount, bc, data=None, walletdb=wdb, coinbase=False).set_id()
    bc.mine_block([tx])
    print(f'Send from {from_addr} to {to_addr} with amount {amount}.')

def getbalance(bc, address):
    pubkey_hash = utils.address2hash(address)
    balance = 0
    UTXOs = bc.find_utxo(pubkey_hash)
    for out in UTXOs:
        balance += out.value
    print(f'Balance of {address}: {balance}')

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    bc = None
    wdb = None
    if hasattr(args, 'wallet'):
        wdb = WalletDB()
        create_wallet(wdb)


    if args.create is not None:
        bc = create_blockchain(args.create)
    
    if hasattr(args, 'addblock'):
        if bc is None:
            bc = Blockchain()
        bc.mine_block(args.transaction)
    if hasattr(args, 'printchain'):
        if bc is None:
            bc = Blockchain()
        print_blockchain(bc)
    if hasattr(args, 'printblock'):
        if bc is None:
            bc = Blockchain()
        print_blockchain(bc, args.height)
    if hasattr(args, 'balance_address'):
        if bc is None:
            bc = Blockchain()
        getbalance(bc, args.balance_address)

    if hasattr(args, 'send_from') and hasattr(args, 'send_to') and hasattr(args, 'send_amount'):
        if wdb is None:
            wdb = WalletDB()
        if bc is None:
            bc = Blockchain()
        send(bc, wdb, args.send_from, args.send_to, args.send_amount)
    
