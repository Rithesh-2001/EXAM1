from web3 import Web3
import json
import time

# Connect to the Ganache blockchain
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
assert web3.is_connected(), "Failed to connect to Ethereum network"

# Set default account from Ganache
web3.eth.default_account = web3.eth.accounts[0]

# Load the contract ABI (replace this with your own ABI)
contract_abi = json.loads('''[
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_uniqueID",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_hashCode",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_unlockTime",
				"type": "uint256"
			}
		],
		"name": "storeHashCode",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getCurrentTime",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_uniqueID",
				"type": "string"
			}
		],
		"name": "getUnlockTime",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "hashcodes",
		"outputs": [
			{
				"internalType": "string",
				"name": "hashCode",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "unlockTime",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_uniqueID",
				"type": "string"
			}
		],
		"name": "revealHashCode",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]''')  # Replace with your contract ABI

# Contract address (replace this with your deployed contract's address)
contract_address = "0x4ECE963D4960B2358ADa1829c92b1143478cBb55"  # Replace with actual address

# Initialize the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Function to store the hashcode
def store_hash(unique_id, hash_code, unlock_time):
    try:
        tx_hash = contract.functions.storeHashCode(unique_id, hash_code, unlock_time).transact({'gas': 500000})
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f"Transaction successful! Hash stored with ID '{unique_id}' and unlock time {unlock_time}")
    except Exception as e:
        print(f"Error storing hash: {e}")

# Function to retrieve the hashcode (fixed)
def retrive_hash(unique_id):
    try:
        # Access the hashCode and unlockTime from the 'hashcodes' mapping
        hash_data = contract.functions.hashcodes(unique_id).call()
        hash_code = hash_data[0]  # Get the hashCode
        unlock_time_for_id = hash_data[1]  # unlockTime is the second element in the tuple

        current_time = int(time.time())  # Get current time in seconds
        print(f"Unlock time for hashcode with ID '{unique_id}': {unlock_time_for_id}")
        print(f"Current time: {current_time}")

        # Check if the current time is greater than or equal to the unlock time
        if current_time >= unlock_time_for_id:
            try:
                revealed_hash = contract.functions.revealHashCode(unique_id).call()
                print(f"Revealed hashcode for ID '{unique_id}': {revealed_hash}")
                return revealed_hash
            except Exception as e:
                print(f"Error revealing hashcode: {e}")
        else:
            time_remaining = unlock_time_for_id - current_time
            print(f"Hashcode is still locked. Time remaining: {time_remaining} seconds.")
            return None
    except Exception as e:
        print(f"Error retrieving hashcode: {e}")


