import streamlit as st
from web3 import Web3
import json
import requests
import os

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
if not w3.is_connected():
    st.error("Failed to connect to Ganache. Ensure Ganache is running on http://127.0.0.1:7545")
    st.stop()
else:
    st.write("Connected to Ganache")

# Pinata IPFS API credentials
PINATA_API_KEY = "f0a3a96d6777c3963dbd"  # Replace with your Pinata API Key
PINATA_SECRET_API_KEY = "6ca86557ff57f77739f0ef37886ecd01f5c9a124683789b71443133294db520e"  # Replace with your Pinata Secret API Key
PINATA_ENDPOINT = "https://api.pinata.cloud/pinning/pinFileToIPFS"

# Load contract
contract_address = "0xf6F4CD4D0258a0857453C386A5E1B103449fCf0B"  # Replace with your new deployed contract address
if not w3.is_address(contract_address):
    st.error("Invalid contract address in app.py")
    st.stop()

try:
    with open("LandRegistry.abi", "r") as f:
        contract_abi = json.load(f)
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)
except Exception as e:
    st.error(f"Failed to load ABI: {str(e)}. Ensure LandRegistry.abi is correct.")
    st.stop()

# Test admin call
try:
    admin = contract.functions.admin().call()
except Exception as e:
    st.error(f"Failed to call admin() function: {str(e)}. Ensure the contract is deployed correctly.")
    st.stop()

# Wallet and private key input
st.sidebar.header("Connect Wallet")
account = st.sidebar.text_input("Enter your wallet address (from Ganache/MetaMask):")
private_key = st.sidebar.text_input("Enter your private key (for testing only):", type="password")
if not account or not private_key:
    st.warning("Please enter a wallet address and private key")
    st.stop()

# Validate account
if not w3.is_address(account):
    st.error("Invalid wallet address")
    st.stop()
try:
    balance = w3.eth.get_balance(account)
    st.sidebar.write(f"Account Balance: {w3.from_wei(balance, 'ether')} ETH")
    if balance < w3.to_wei(1, 'ether'):
        st.error("Account has insufficient ETH. Use a Ganache account with ~100 ETH.")
        st.stop()
except Exception as e:
    st.error(f"Failed to fetch balance: {str(e)}")
    st.stop()

# Check if admin
is_admin = account.lower() == admin.lower()

# Sidebar navigation
menu = ["Home", "Register Land", "View Land", "Transfer Ownership", "View All Lands", "View My Lands"]
choice = st.sidebar.selectbox("Menu", menu if is_admin else menu[2:])

# Sign transaction function
def send_transaction(function, account, private_key):
    try:
        nonce = w3.eth.get_transaction_count(account)
        tx = function.build_transaction({
            "from": account,
            "nonce": nonce,
            "gas": 6000000,
            "gasPrice": w3.eth.gas_price * 2
        })
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        if receipt.status == 0:
            raise Exception(f"Transaction reverted: {receipt}")
        return tx_hash
    except Exception as e:
        raise Exception(f"Transaction failed: {str(e)}")

# Home Page
if choice == "Home":
    st.header("Welcome to the Land Registry System")
    st.write("Use the sidebar to navigate. Connect your wallet to interact with the blockchain.")
    if is_admin:
        st.write("You are logged in as Admin.")
    else:
        st.write("You are logged in as a User.")

# Register Land (Admin Only)
elif choice == "Register Land" and is_admin:
    st.header("Register New Land")
    location = st.text_input("Location (e.g., 123 Main St)")
    area = st.number_input("Area (sq. ft.)", min_value=1, step=1)
    price = st.number_input("Price (ETH)", min_value=0, step=1)
    owner = st.text_input("Owner Wallet Address")
    document = st.file_uploader("Upload Land Document (PDF/Image)", type=["pdf", "jpg", "png", "jpeg"])
    
    if st.button("Register Land"):
        try:
            if not w3.is_address(owner):
                st.error("Invalid owner wallet address")
                st.stop()
            document_hash = ""
            if document:
                temp_file_path = "temp_document"
                with open(temp_file_path, "wb") as f:
                    f.write(document.read())
                with open(temp_file_path, "rb") as file:
                    files = {"file": (document.name, file)}
                    headers = {
                        "pinata_api_key": PINATA_API_KEY,
                        "pinata_secret_api_key": PINATA_SECRET_API_KEY
                    }
                    response = requests.post(PINATA_ENDPOINT, files=files, headers=headers)
                    if response.status_code != 200:
                        raise Exception(f"Failed to upload to Pinata: {response.text}")
                    document_hash = response.json()["IpfsHash"]
                try:
                    os.remove(temp_file_path)
                except Exception as e:
                    st.warning(f"Could not delete temporary file: {str(e)}")
                st.write(f"Document uploaded to IPFS: {document_hash}")
            function = contract.functions.registerLand(location, area, price, owner, document_hash)
            tx_hash = send_transaction(function, account, private_key)
            st.success(f"Land registered! Transaction Hash: {tx_hash.hex()}")
            if document_hash:
                st.write(f"View document: https://ipfs.io/ipfs/{document_hash}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# View Land
elif choice == "View Land":
    st.header("View Land Details")
    land_id = st.number_input("Enter Land ID", min_value=1, step=1)
    if st.button("View Land"):
        try:
            land = contract.functions.viewLand(land_id).call()
            if land[0] == 0:
                st.error("Land ID does not exist or is not registered.")
            else:
                st.write(f"**Land ID**: {land[0]}")
                st.write(f"**Location**: {land[1]}")
                st.write(f"**Area**: {land[2]} sq. ft.")
                st.write(f"**Price**: {land[3]} ETH")
                st.write(f"**Owner**: {land[4]}")
                st.write(f"**Registered**: {'Yes' if land[5] else 'No'}")
                if land[6]:
                    st.write(f"**Document**: [View on IPFS](https://ipfs.io/ipfs/{land[6]})")
                else:
                    st.write("**Document**: No document uploaded")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Transfer Ownership
elif choice == "Transfer Ownership":
    st.header("Transfer Land Ownership")
    land_id = st.number_input("Land ID", min_value=1, step=1)
    new_owner = st.text_input("New Owner Wallet Address")
    if st.button("Transfer Ownership"):
        try:
            if not w3.is_address(new_owner):
                st.error("Invalid new owner wallet address")
                st.stop()
            function = contract.functions.transferOwnership(land_id, new_owner)
            tx_hash = send_transaction(function, account, private_key)
            st.success(f"Ownership transferred! Transaction Hash: {tx_hash.hex()}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# View All Lands
elif choice == "View All Lands":
    st.header("All Registered Lands")
    try:
        lands = contract.functions.getAllLands().call()
        if not lands:
            st.write("No lands registered yet.")
        for land in lands:
            if land[5]:
                st.write(f"**ID**: {land[0]}, **Location**: {land[1]}, **Area**: {land[2]} sq. ft., **Price**: {land[3]} ETH, **Owner**: {land[4]}, **Document**: [{land[6] or 'No document'}](https://ipfs.io/ipfs/{land[6]})")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# View My Lands
elif choice == "View My Lands":
    st.header("Your Lands")
    try:
        land_ids = contract.functions.getOwnerLands(account).call()
        if not land_ids:
            st.write("You don't own any lands.")
        for land_id in land_ids:
            land = contract.functions.viewLand(land_id).call()
            st.write(f"**ID**: {land[0]}, **Location**: {land[1]}, **Area**: {land[2]} sq. ft., **Price**: {land[3]} ETH, **Document**: [{land[6] or 'No document'}](https://ipfs.io/ipfs/{land[6]})")
    except Exception as e:
        st.error(f"Error: {str(e)}")