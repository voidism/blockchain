import argparse

from blockchain import Blockchain
from proof_of_work import Pow

def get_parser():
    parser = argparse.ArgumentParser()
    # A print command
    parser.add_argument('--print', dest='print', action='store_true')
    # A createblockchain command
    parser.add_argument(
        '--create', type=str, help='ADDRESS of create blockchain')
    # A add block command
    parser.add_argument(
        '--add', type=str, help='DATA of create block')
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

def print_blockchain(bc=None):
    for block in bc.blocks:
        #print("Prev. hash: {0}".format(block.prev_block_hash))
        #print("Hash: {0}".format(block.hash))
        print(block)
        pow = Pow(block)
        print("PoW: {0}".format(pow.validate()))


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    bc = None
    if args.create is not None:
        bc = create_blockchain(args.create)
    
    if bc is None:
        bc = Blockchain()

    if args.add is not None:
        bc.mine_block(args.add)

    if args.print:
        print_blockchain(bc)
