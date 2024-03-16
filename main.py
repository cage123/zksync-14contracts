from web3 import Web3
import time, random

from cryptography.fernet import Fernet
from getpass import getpass

RPC = ''
TO_SLEEP_TXS = [20, 180]
TO_SLEEP_BETWEEN_ACCS = [7000, 14500]
MAX_GAS = 100
TXS_COUNT = [11, 14] # 14 max

# Don't touch
w3 = Web3(Web3.HTTPProvider(RPC))
CONTRACTS = [
    hex(0x78e1F126a1BAE67bBC05A92CF2Bc171C69ee250a),
    hex(0xcB27b19c27e316f2deE2f07123716F36368C9e97),
    #hex(0x0C4E0F1Ff3B200db601b5A27adBaD288e804A35B),
    hex(0x28702B2b58cCb5927b53aF91E5dC63270273d4C3),
    hex(0x353a12B0D46618c513bF5313AB7DfFB01227C234),
    hex(0x8baCe5229771d2909924B055aCd2f109EB4cf8a8),
    hex(0x893feD28e2d1599a513498d6CF6D0Fb5dA5fbbd4),
    hex(0xA7f0A6162567E2E9d77f81C8bc7a2E18F19f5d28),
    hex(0xA7Fb8cd35409062a7D811535B7b0c2274335D5bD),
    hex(0x2c38130dfF9097F9486Ee0A53f5261e9c6acd6ad),
    hex(0xFcc21e03b25BC8cA918D497fb014fa3491503c0c),
    hex(0x9FB6Ca27D20E569E5c8FeC359C9d33D468d2803C),
    hex(0x7a209041eAD28cBd830f3e73289f7b89DE6C805C),
    hex(0xD753A8a1155eFC50a52B7088D410f39f856225E2),
    hex(0xC6e980CC272767766592BcBb9763665983CDC4a0),
]

if __name__ == '__main__':
    Dkey = getpass('Input key: ')
    FFF = Fernet(Dkey)
    
    with open('wallets.txt', 'r') as f:
        data = f.read().splitlines()
    for privatekey in data:
        account = w3.eth.account.from_key(FFF.decrypt(privatekey.encode()).decode())
        account_address = account.address
        
        random.shuffle(CONTRACTS)
        txs_count = random.randint(TXS_COUNT[0], TXS_COUNT[1])
        txs = 0
        
        print(f'{account_address} - {txs_count} TXs')
        
        for contract in CONTRACTS:
            txs += 1
            if txs > txs_count:
                break
            
            nonce = w3.eth.get_transaction_count(account_address)
            
            w3_eth = Web3(Web3.HTTPProvider('https://rpc.ankr.com/eth'))
            while True:
                gasPrice = w3_eth.eth.gas_price
                gas = w3_eth.from_wei(gasPrice, 'gwei')
                if gas < MAX_GAS:
                    break
                print(f"{gas} GWEI сейчас / Жду газа {MAX_GAS} GWEI",end="", flush=True)
                time.sleep(20)
                print("\033[K", end="\r", flush=True)
            
            gasPrice = w3.eth.gas_price
            try:
                transaction = {
                    'chainId': 324,
                    'from': account_address,
                    'to': w3.to_checksum_address(contract),
                    'value': w3.to_wei('0', 'ether'),
                    'gas': 600000,
                    'maxFeePerGas': gasPrice,
                    'maxPriorityFeePerGas': int(gasPrice),
                    'nonce': nonce,
                    'data': 0x30c47752,
                }
                
                signed_transaction = account.sign_transaction(transaction)
                txn_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
                txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
                
                print(f'{txs}/{txs_count} | https://era.zksync.network/tx/{(w3.to_hex(txn_hash))}')
                    
                to_sleep = random.randint(TO_SLEEP_TXS[0], TO_SLEEP_TXS[1])
                print(f'Sleep {to_sleep} sec.')
                time.sleep(to_sleep)
                
            except Exception as error:
                print(f'{txs}/{txs_count} | {account.address} Error: {error}')
                to_sleep = random.randint(TO_SLEEP_TXS[0], TO_SLEEP_TXS[1])
                print(f'Sleep {to_sleep} sec.')
                time.sleep(to_sleep)
        
        to_sleep = random.randint(TO_SLEEP_BETWEEN_ACCS[0], TO_SLEEP_BETWEEN_ACCS[1])
        print(f'Sleep {to_sleep} sec.')
        time.sleep(to_sleep)