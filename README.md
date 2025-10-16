# Decentralized-Land-Registry-System

A blockchain-based application for secure and transparent land record management using Ethereum and IPFS. Built with Solidity, Streamlit, web3.py, Ganache, MetaMask, and Pinata, this system enables admins to register land records, store documents on IPFS, and allows users to view or transfer ownership. Designed for a showcase, it features a user-friendly interface and one-click deployment via setup.bat.Table of ContentsOverview (#overview)
Features (#features)
Tech Stack (#tech-stack)
Prerequisites (#prerequisites)
Installation (#installation)
Usage (#usage)
Demo (#demo)
Troubleshooting (#troubleshooting)
Contributing (#contributing)
License (#license)

OverviewThe Decentralized Land Registry System leverages Ethereum smart contracts for immutable land records and IPFS for decentralized document storage. Admins register lands with details (e.g., location, area, price, owner, document), while users can view records or transfer ownership. The system uses Ganache for a local blockchain and Streamlit for a web interface, with a one-click setup for easy deployment.FeaturesLand Registration: Admins register land with details and upload documents (e.g., 3rd.pdf) to IPFS via Pinata.
View Land: Retrieve land details by ID, with robust error handling for invalid IDs.
Transfer Ownership: Securely transfer land to a new owner, with authorization checks.
List Lands: View all registered lands or user-owned lands.
Gas Fees: Transactions (e.g., registration, transfer) incur small test ETH fees (~0.004 ETH) for blockchain processing, not sent to any recipient.
User Interface: Streamlit app at http://localhost:8501 for seamless interaction.
Block Generation: Each state-changing transaction (e.g., registration) creates a new block, visible in the UI.

Tech StackSmart Contract: Solidity (^0.8.20, LandRegistry.sol)
Frontend: Streamlit (app.py)
Blockchain: Ganache (http://127.0.0.1:7545, Chain ID: 1337)
Wallet: MetaMask for transaction signing
IPFS: Pinata for decentralized document storage
Dependencies: web3.py, py-solc-x, requests (Python 3.12.10)
Setup: setup.bat for Windows

PrerequisitesNode.js: Install from nodejs.org (v16 or later).
Python 3.12.10: Install from python.org.
MetaMask: Browser extension for Ethereum wallet.
Pinata Account: Sign up at pinata.cloud for API keys.
Windows: Tested on Windows 10/11.

InstallationClone the Repository:bash

git clone https://github.com/Harshil2498/Decentralized-Land-Registry-System.git
cd land-registry

Set Up Python Environment:bash

python -m venv venv
venv\Scripts\activate
pip install streamlit web3 py-solc-x requests

Install Ganache:bash

npm install -g ganache@latest

Configure Pinata:Update app.py with your Pinata API keys:python

PINATA_API_KEY = "your_pinata_api_key"
PINATA_SECRET_API_KEY = "your_pinata_secret_api_key"

Run Setup Script:bash

setup.bat

Starts Ganache with 10 accounts (~100 ETH each) and Streamlit.
Creates ganache_data for persistent blockchain state.

UsageDeploy Smart Contract:Open Remix IDE.
Paste LandRegistry.sol (Solidity ^0.8.20).
Compile and deploy:Environment: Injected Provider (MetaMask).
Connect MetaMask to Ganache (http://127.0.0.1:7545, Chain ID: 1337).
Use first Ganache account (~100 ETH).
Set gas limit: 6,000,000.

Copy contract address and ABI to LandRegistry.abi.
Update app.py:python

contract_address = "your_contract_address"

Run Application:Execute setup.bat or:bash

ganache --db ganache_data --gasLimit 8000000 --accounts 10 --defaultBalanceEther 100
streamlit run app.py

Open http://localhost:8501.

Interact:Connect Wallet: Enter admin account address and private key (from Ganache).
Register Land (Admin): Input location (e.g., 123 Main St), area (1000), price (1), owner address, document (3rd.pdf). Outputs transaction hash, IPFS link, gas cost (~0.004 ETH), block number increase.
View Land: Enter ID (1) to see details and IPFS link.
Transfer Ownership: Transfer land to another address, with gas cost and block increase.
View All/My Lands

