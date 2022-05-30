import os
import json
#from grpc import stream_unary_rpc_method_handler
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

load_dotenv("key.env")

# Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################
st.title("Art Auction Fundraiser")
st.markdown("### Ukraine aid auction")

st.image('https://media2.giphy.com/media/xT5LMESHbV1KLGMsq4/giphy.gif')

st.markdown("## Welcome to our Art Auction Fundraiser, to support non-profit organizations, This market serves to raise funds for the Ukraine invation by auctioning art donated by different artist, please place a bid!!  ")


# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('./contracts/compiled/certificate_abi.json')) as f:
        certificate_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = Web3.toChecksumAddress(0x67d5954bc545fd3c31204f4cf7819e48bcff7954)

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
# Helper functions to pin files and json to Pinata
################################################################################


def pin_artwork(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file)

    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash


def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash



    ################################################################################
    # options page
    ################################################################################

account_selection = ["Artist", "Buyer", "Donor"]

account = st.radio('Are you a Artist Donator , or you are a Buyer?', account_selection)

if account == "Artist":
    
    st.markdown("## Register New Artwork")
    address = st.text_input("artist_address")
    artwork_name = st.text_input("Enter the name of the artwork")
    artist_name = st.text_input("Enter the artist name")
    initial_appraisal_value = st.text_input("Enter the initial appraisal amount")

    # Use the Streamlit `file_uploader` function create the list of digital image file types(jpg, jpeg, or png) that will be uploaded to Pinata.
    file = st.file_uploader("Upload Artwork", type=["jpg", "jpeg", "png"])

    if st.button("Register Artwork"):
        # Use the `pin_artwork` helper function to pin the file to IPFS
        artwork_ipfs_hash = pin_artwork(artwork_name, file)

        artwork_uri = f"ipfs://{artwork_ipfs_hash}"

        tx_hash = contract.functions.registerArtwork(
            address,
            artwork_name,
            artist_name,
            int(initial_appraisal_value),
            artwork_uri
        ).transact({'from': address, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))
        st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        st.markdown(f"[Artwork IPFS Gateway Link](https://ipfs.io/ipfs/{artwork_ipfs_hash})")
    st.markdown("---")

    #st.buttom("create auction")
    #if st.button("create auction"):
    #    creacteAuction = contract.functions.createAuction("token_id")

if account == "Donor":
    st.sidebar.radio('Select one:', ['Bitcoin', 'Etherium', "Dogecoin", "XRP", "Solana"])
    amount = st.text_input("Enter amount you want to donate");
    contributor_address = st.text_input("Enter account address");
    
    if st.button("donate now"):
        st.text('tanks for your donations')
        st.balloons()
else:
    st.text_input('Enter account address')





#st.image('data:image/jpeg;base64,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HHiRHLx8ceJG5cxp8qvgj7DmFPlV8EfYnQ46flvT0id1Q/dwrDeXh448SI5eHjjxI3PmFPlV8EfYcxp8qvgj7DQ46flvU+kbuqH7uFYXy8fHHiR1tVdG2YvE1cmm6arYWW2r6EVBqSipdTk2ksl2Zmvcxp8qvgj7H7RrSSSSSXUkkkjdDktkbw4urTsotFpy9JNGY2sDa3VrW73BewAdNcJAAEQABEAARAAEQABEIyJARV/WLV+OJXKV5RuS6+pWekvX1KdfXjorkHXjHHqVUa7pwfpmuhl9+RqAyKE+T4pn594JxoaV8br1dgt8sLcwUIGFRWnheqfqfoC2qTxWJjsWODhXTmpOqLacnNrdtvJdTaSXxLiQiS3FE2JgYwUAVWSR0jy9xvKAA2LBAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEQABEAARAAEX//2Q==')
st.markdown("## place a bid! ")


st.success("Congratulation you won the auction")
#st.balloons()
#if st.button("Place bid")



@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('./contracts/compiled/AuctionMarket_abi.json')) as f:
        certificate_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = Web3.toChecksumAddress(0x73dfd5402736b48c6dd9532e60dc6d5c160d093)

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )
    # Return the contract from the function
    return contract


# Load the contract
second_contract = load_contract()

bid = second_contract.functions.bid(msg.sender)


