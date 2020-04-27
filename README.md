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
New address: LQ8hfLNaYRSup3nTKZp7StJdBoLuJ9Lovj
```

### 2. Create Blockchain

Bind an address to the Blockchain.
It will accept the reward of the Genesis block.

```
./pseudoBitcoin createblockchain -address LQ8hfLNaYRSup3nTKZp7StJdBoLuJ9Lovj
```

The first coinbase block is created.
I set all reward values to 100.

```
Mining the block containing: [
CoinbaseTx(
	id='1bcba98abd25ac13358173b852d6f3e6b4b3f1b98587bf484e6f24c198067de3',
	vin=[TXInput(tx_id=b'', value=-1, script_sig=None, public_key='The Times 03/Jan/2009 Chancellor on brink of second bailout for banks')],
	vout=[TXOutput(value=100, pubkey_hash=b'5\xda\\J\xec\xf7xC&\x9d\xe4\xd1\x83\xa2\x12\xc4\xd2\xe0\xd1\xea')],
	time='1587960306.615166')
]
Create Blockchain; Reward sent to LQ8hfLNaYRSup3nTKZp7StJdBoLuJ9Lovj
```

### 3. Get Balance of a Wallet

Run 
```
./pseudoBitcoin getbalance -address LQ8hfLNaYRSup3nTKZp7StJdBoLuJ9Lovj
```

We can see the balance of the wallet.

```
Balance of LQ8hfLNaYRSup3nTKZp7StJdBoLuJ9Lovj: 100
```

### 4. Send Transaction to Another Wallet

Be sure to obtain another wallet, for example `LRqUDNX1jFxYdmjjhphGARLfAaMHAzuiDe`.

Now we send a transaction from A to B with amount=10.
- A: `LQ8hfLNaYRSup3nTKZp7StJdBoLuJ9Lovj`
- B: `LRqUDNX1jFxYdmjjhphGARLfAaMHAzuiDe`
```
./pseudoBitcoin send -from LQ8hfLNaYRSup3nTKZp7StJdBoLuJ9Lovj -to LRqUDNX1jFxYdmjjhphGARLfAaMHAzuiDe -amount 10
```

You can specify the amount of the transaction after argument `-amount`.

Two transaction will be sent:
1. The transaction you specified from A to B with amount=10.
2. A reward coinbase transaction (amount=100) for mining this transaction. We did not implement the network. Thus, we simply send the reward to A, who creates this transaction and mining the block.

> If the sent amount(=10) is lower than the amount of the coinbase reward(=100), the sender will gain more coins after sending the transaction.

```
Mining the block containing: [
UTXOTx(
	id='e7acc362eb551bbe11cd4278d4d66a5dae6d107bf2e203df5d732474020e7ee0',
	vin=[TXInput(tx_id=b'1bcba98abd25ac13358173b852d6f3e6b4b3f1b98587bf484e6f24c198067de3', value=0, script_sig=None, public_key='04e11ae0073883065818fb8f421dde2351473227500d9a7881e23776b4c8615b8384f0f784a8cde109e34b4dc8073ede0c8939b63d38ec4d2919c1b8a22857c82d')],
	vout=[TXOutput(value=10, pubkey_hash=b'H\x88P\xb1\xc3"2X\xa3\xf8\xecp\x80\xc1\xf4\x18\x85m\xbb\x98'), TXOutput(value=90, pubkey_hash=b'5\xda\\J\xec\xf7xC&\x9d\xe4\xd1\x83\xa2\x12\xc4\xd2\xe0\xd1\xea')],
	time='1587960390.382575'),
CoinbaseTx(
	id='39ec0692769592d9973e8bdbaa7e215376ffb0edf789a5ebc6cdec12da589300',
	vin=[TXInput(tx_id=b'', value=-1, script_sig=None, public_key='Reward to LQ8hfLNaYRSup3nTKZp7StJdBoLuJ9Lovj')],
	vout=[TXOutput(value=100, pubkey_hash=b'5\xda\\J\xec\xf7xC&\x9d\xe4\xd1\x83\xa2\x12\xc4\xd2\xe0\xd1\xea')],
	time='1587960390.382723')
]
00006484188d398c875f56578e07830e1e2d450fce4b734cb85a4db0300e4992
Success!
Send from LQ8hfLNaYRSup3nTKZp7StJdBoLuJ9Lovj to LRqUDNX1jFxYdmjjhphGARLfAaMHAzuiDe with amount 10.
```

Now we can use `getbalance` to see the balance of A and B.
- A should have: 100 + (-10+100) = 190
- B should have: 10
```
./pseudoBitcoin getbalance -address LQ8hfLNaYRSup3nTKZp7StJdBoLuJ9Lovj

Balance of LQ8hfLNaYRSup3nTKZp7StJdBoLuJ9Lovj: 190

./pseudoBitcoin getbalance -address LRqUDNX1jFxYdmjjhphGARLfAaMHAzuiDe

Balance of LRqUDNX1jFxYdmjjhphGARLfAaMHAzuiDe: 10
```

### 5. Print Chain and Blocks

To print the whole chain, run
```
./pseudoBitcoin printchain
```

All blocks will be printed from newer one to older one, and proof of work (PoW) will also be evaluated.  
We can check that the second block (older) has the same hash as the prev_hash of the first block (newer).

```
+- Block ---------
| hash <=== 00006484188d398c875f56578e07830e1e2d450fce4b734cb85a4db0300e4992
| time = b'1587960390'
| data = [
UTXOTx(
	id='e7acc362eb551bbe11cd4278d4d66a5dae6d107bf2e203df5d732474020e7ee0',
	vin=[TXInput(tx_id=b'1bcba98abd25ac13358173b852d6f3e6b4b3f1b98587bf484e6f24c198067de3', value=0, script_sig=None, public_key='04e11ae0073883065818fb8f421dde2351473227500d9a7881e23776b4c8615b8384f0f784a8cde109e34b4dc8073ede0c8939b63d38ec4d2919c1b8a22857c82d')],
	vout=[TXOutput(value=10, pubkey_hash=b'H\x88P\xb1\xc3"2X\xa3\xf8\xecp\x80\xc1\xf4\x18\x85m\xbb\x98'), TXOutput(value=90, pubkey_hash=b'5\xda\\J\xec\xf7xC&\x9d\xe4\xd1\x83\xa2\x12\xc4\xd2\xe0\xd1\xea')],
	time='1587960390.382575'),
CoinbaseTx(
	id='39ec0692769592d9973e8bdbaa7e215376ffb0edf789a5ebc6cdec12da589300',
	vin=[TXInput(tx_id=b'', value=-1, script_sig=None, public_key='Reward to LQ8hfLNaYRSup3nTKZp7StJdBoLuJ9Lovj')],
	vout=[TXOutput(value=100, pubkey_hash=b'5\xda\\J\xec\xf7xC&\x9d\xe4\xd1\x83\xa2\x12\xc4\xd2\xe0\xd1\xea')],
	time='1587960390.382723')
]
|nonce = 26019
| prev ===> 0000d94617193eb969700a5a7f0613f6e77dfbf690eaa2021a3f442f0a6dff95
+-----------------
PoW: True

+- Block ---------
| hash <=== 0000d94617193eb969700a5a7f0613f6e77dfbf690eaa2021a3f442f0a6dff95
| time = b'1587960306'
| data = [ ...

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
- [x] 5. Transaction(advanced): Mining reward(2%), Merkle tree(8%) --> 10%
- [ ] ~~6. Network: P2P(10%) or Server-Client(7%) --> 10%~~
- [ ] ~~Other features: Proof of ???, Special design --> 5%~~

## Reference
1. blockchain-py: https://github.com/yummybian/blockchain-py
2. blockchain-tutorial: https://liuchengxu.gitbooks.io/blockchain-tutorial/content/