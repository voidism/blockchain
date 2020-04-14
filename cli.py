import argparse

from blockchain import Blockchain
from proof_of_work import Pow

def get_parser():
    parser = argparse.ArgumentParser()
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
    # A createblockchain command
    parser.add_argument(
        '--create', type=str, help='ADDRESS of create blockchain')
    # A getbalance command
    parser.add_argument(
        '--getbalance', type=str, help='ADDRESS of balance')
    # A send command
    parser.add_argument(
        '--send_from', type=str, help='FROM')
    parser.add_argument(
        '--send_to', type=str, help='TO')
    parser.add_argument(
        '--amount', type=int, dest='send_amount', help='AMOUNT')

    return parser

def create_blockchain(address):
    bc = Blockchain()
    print('Done!')
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


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    bc = None
    if args.create is not None:
        bc = create_blockchain(args.create)
    
    if bc is None:
        bc = Blockchain()

    if hasattr(args, 'addblock'):
        bc.mine_block(args.transaction)

    if hasattr(args, 'printchain'):
        print_blockchain(bc)
    if hasattr(args, 'printblock'):
        print_blockchain(bc, args.height)
