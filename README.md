Blockchain
===

b05901033 電機四 莊永松

## Prerequisites

- python3
- ecdsa
- base58

Install them by `pip3 install -r requirements.txt`

## How to use?

### 1. Create Wallet

Run
```
./pseudoBitcoin createwallet
```

After that, we get a new wallet address.

```
New address: LWLoyXEcE6sB7huq31JzPDt4fFaLUCLiy3
```

### 2. Create Blockchain

Bind an address to the Blockchain.
It will accept the reward of the Genesis block.

```
./pseudoBitcoin createblockchain -address LWLoyXEcE6sB7huq31JzPDt4fFaLUCLiy3
```

The first coinbase block is created.
I set all reward values to 2048.

```
Mining the block containing: [
CoinbaseTx(
	id='603da794609e2b0cfa8d726caa90ec02d02a551fb9be34d54dd1290561ca9a51',
	vin=[TXInput(tx_id=b'', value=-1, script_sig=None, public_key='The Times 03/Jan/2009 Chancellor on brink of second bailout for banks')],
	vout=[TXOutput(value=2048, pubkey_hash=b"y\xf5`\x87\x8fl,N\x8bM\xe2'j:s\r\xea\xa4\x1a\x05")]
)
]
Create Blockchain; Reward sent to LWLoyXEcE6sB7huq31JzPDt4fFaLUCLiy3
```

### 3. Get Balance of a Wallet

Run 
```
./pseudoBitcoin getbalance -address LWLoyXEcE6sB7huq31JzPDt4fFaLUCLiy3
```

We can see the balance of the wallet.

```
Balance of LWLoyXEcE6sB7huq31JzPDt4fFaLUCLiy3: 2048
```

### 4. Send Transaction to Another Wallet

Be sure to obtain another wallet, for example `LPYim5veN6s24RRtvhqMy172u77mMSRunX`.

Now we send a transaction from A to B with amount=10.
- A: `LWLoyXEcE6sB7huq31JzPDt4fFaLUCLiy3`
- B: `LPYim5veN6s24RRtvhqMy172u77mMSRunX`
```
./pseudoBitcoin send -from LWLoyXEcE6sB7huq31JzPDt4fFaLUCLiy3 -to LPYim5veN6s24RRtvhqMy172u77mMSRunX -amount 10
```

You can specify the amount of the transaction after argument `-amount`.

Two transaction will be sent:
1. The transaction you specified from A to B with amount=10.
2. A reward coinbase transaction for mining this transaction. We did not implement the network. Thus, we simply send the reward to A, who create this transaction and mining the block.
```
Mining the block containing: [
UTXOTx(
	id='d5dc9bb600b3d156a95633c632f490c716b2e299b837c7a7a27d1f3cff8c2d35',
	vin=[TXInput(tx_id=b'603da794609e2b0cfa8d726caa90ec02d02a551fb9be34d54dd1290561ca9a51', value=0, script_sig=None, public_key='04600296660ae3586010c945de710c0ef1cb00207c23ede7244ceb0dda70bec017174161d74f8080d0833e250f98f4f39ea131449b2ff20a4453ba9ae9f07f79b1')],
	vout=[TXOutput(value=10, pubkey_hash=b'/m"\xa5\xf31\xa2\x9f6\xa9\n\xab\x9c\x94\xd9\xac\xf4y\xce\xa4'), TXOutput(value=2038, pubkey_hash=b"y\xf5`\x87\x8fl,N\x8bM\xe2'j:s\r\xea\xa4\x1a\x05")]
)
,
CoinbaseTx(
	id='e21d7311a3c0af6f99fe07c6f4c36e0926f1ff1b6a41dd3e59c165c369f9b9cc',
	vin=[TXInput(tx_id=b'', value=-1, script_sig=None, public_key='Reward to LWLoyXEcE6sB7huq31JzPDt4fFaLUCLiy3')],
	vout=[TXOutput(value=2048, pubkey_hash=b"y\xf5`\x87\x8fl,N\x8bM\xe2'j:s\r\xea\xa4\x1a\x05")]
)
]
0000b510f9f8214e937a4d90fdf8d580124fc15de9fd01c9ac1f85c680c93489
Success!
Send from LWLoyXEcE6sB7huq31JzPDt4fFaLUCLiy3 to LPYim5veN6s24RRtvhqMy172u77mMSRunX with amount 10.
```

### 5. Print Chain and Blocks

To print the whole chain, run
```
./pseudoBitcoin printblock -height 3
```

All blocks will be printed, and proof of work (PoW) will also be evaluated.

```

+- Block ---------
| hash <=== 000023c11c30a6a7bc4135475cba67784e2ae5a27ea576579e92c189b5620cf2
| time = b'1587922677'
| data = [
UTXOTx(
	id='af15102ee0d58d85905cfef190abc7ef08110756508fcbdbf5d0582df245e8db',
	vin=[TXInput(tx_id=b'2d988778b8960d69b5394644391e90e56261988b5951731ba404b10d9537ecbf', value=1, script_sig=None, public_key='04600296660ae3586010c945de710c0ef1cb00207c23ede7244ceb0dda70bec017174161d74f8080d0833e250f98f4f39ea131449b2ff20a4453ba9ae9f07f79b1')],
	vout=[TXOutput(value=10, pubkey_hash=b'/m"\xa5\xf31\xa2\x9f6\xa9\n\xab\x9c\x94\xd9\xac\xf4y\xce\xa4'), TXOutput(value=2008, pubkey_hash=b"y\xf5`\x87\x8fl,N\x8bM\xe2'j:s\r\xea\xa4\x1a\x05")]
)
,
CoinbaseTx(
	id='e21d7311a3c0af6f99fe07c6f4c36e0926f1ff1b6a41dd3e59c165c369f9b9cc',
	vin=[TXInput(tx_id=b'', value=-1, script_sig=None, public_key='Reward to LWLoyXEcE6sB7huq31JzPDt4fFaLUCLiy3')],
	vout=[TXOutput(value=2048, pubkey_hash=b"y\xf5`\x87\x8fl,N\x8bM\xe2'j:s\r\xea\xa4\x1a\x05")]
)
]
|nonce = 80482
| prev ===> 00005fd7eb0ff06db43e224e856ad41c366b54cfa61b9f2828324572b2fc3ab4
+-----------------
PoW: True

+- Block ---------

...
```

To print part of the blocks, run

```
./pseudoBitcoin printblock -height 3
```
use `-height` to specify the number of blocks to print.

##  Functionalities
1~5 are completed.
- [x] 1. Prototype: Block(10%), Blockchain(10%), Proof-of-Work(20%) --> 40%
- [x] 2. Persistence: Database(20%), Client(20%) --> 40%
- [x] 3. Transaction(basic): UTXO(5%) or Account model(2%) --> 5%
- [x] 4. Address: Sign & Verify(5%) --> 5%
- [x] 5. Transaction(advanced) Mining reward(2%), Merkle tree(8%) --> 10%
- [ ] ~~6. Network P2P(10%) or Server-Client(7%) --> 10%~~
- [ ] ~~Other features Proof of ???, Special design --> 5%~~