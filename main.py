from blockchain import Blockchain
from proof_of_work import Pow

if __name__ == '__main__':
    bc = Blockchain()
    bc.add_block("Send 1 BTC to Ivan")
    bc.add_block("Send 2 more BTC to Ivan")

    for block in bc.blocks:
        #print("-----")
        #print("Prev: ===> {0}".format(block.prev_block_hash))
        #print("Data: {0}".format(block.data))
        #print("Hash: <=== {0}".format(block.hash))
        print(block)
        pow = Pow(block)
        print("PoW: {0}".format(pow.validate()))
