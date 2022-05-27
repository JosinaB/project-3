import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

load_dotenv("key.env")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################

# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('./contracts/compiled/certificate_abi.json')) as f:
        certificate_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )
    # Return the contract from the function
    return contract


# Load the contract
contract = load_contract()


################################################################################
# Award Certificate
################################################################################

accounts = w3.eth.accounts
account = accounts[0]
student_account = st.selectbox("Select Account", options=accounts)
certificate_details = st.text_input("Certificate Details", value="Art Ownership Certification")
if st.button("Award Certificate"):
    contract.functions.awardCertificate(student_account, certificate_details).transact({'from': account, 'gas': 1000000})

################################################################################
# Display Certificate
################################################################################
certificate_id = st.number_input("Enter a Certificate Token ID to display", value=0, step=1)
if st.button("Display Certificate"):
    # Get the certificate owner
    certificate_owner = contract.functions.ownerOf(certificate_id).call()
    st.write(f"The certificate was awarded to {certificate_owner}")

    # Get the certificate's metadata
    certificate_uri = contract.functions.tokenURI(certificate_id).call()
    st.write(f"The certificate's tokenURI metadata is {certificate_uri}")


def pin_cert(song_name, cert_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(cert_file.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "name": cert_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash

    ################################################################################
# Award Certificate
################################################################################

accounts = w3.eth.accounts
account = accounts[0]
cert_name = st.text_input("song Name: ")
student_account = st.selectbox("Select Account", options=accounts)
certificate_details = st.text_input("Certificate Details", value="Certification Of Ownership")
file = st.file_uploader("Upload Certificate", type=["ogg", "wma", "mp3", "AAC", "FLAC", "AIFF", "WAV"])
if st.button("Award Certificate"):
    cert_ipfs_hash = pin_cert(cert_name, file)
    cert_uri = f"ipfs://{cert_ipfs_hash}"
    tx_hash = cert_contract.functions.registerCertificate(
        student_account,
        cert_uri
    ).transact({'from': student_account, 'gas': 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Transaction receipt mined:")
    st.write(dict(receipt))
    st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
    st.markdown(f"[Certificate IPFS Gateway Link](https://ipfs.io/ipfs/{cert_ipfs_hash})")
st.markdown("---")