import os
import json

from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
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

#st.image('https://www.networkforgood.com/wp-content/uploads/shutterstock_1703436250-scaled.jpg')
image4 = Image.open('./images/Evacuation.png')
st.image(image4, caption='Evacuation')

st.markdown("## Welcome to our Art Auction Fundraiser, to support non-profit organizations, This market serves to raise funds for the Ukraine invasion by auctioning art donated by different artist, please place a bid!!  ")


# Cache the contract on load
@st.cache(allow_output_mutation=True)
# Define the load_contract function
def load_contract():

    # Load Art Gallery ABI
    with open(Path('./contracts/compiled/certificate_abi.json')) as f:
        certificate_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = Web3.toChecksumAddress(0x88fe134209d8e6bbc8cff4a081c23fc8b0aba365)

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )
    # Return the contract from the function
    return contract


# Load the contract
contract = load_contract()


# Define the second_contract function
def load_second_contract():

    # Load Art Gallery ABI
    with open(Path('./contracts/compiled/AuctionMarket_abi.json')) as f:
        certificate_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = Web3.toChecksumAddress(0x67d5954bc545fd3c31204f4cf7819e48bcff7954)

    # Get the contract
    second_contract = w3.eth.contract(
        address=contract_address,
        abi=certificate_abi
    )
    # Return the contract from the function
    return second_contract


# Load the contract
second_contract = load_contract()




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

account = st.radio('Are you an Artist, Buyer , or Donor?', account_selection)
    #####################################################################################
    #### Artist
    #####################################################################################
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

    if st.button("art_collection"):
        art_collection = contract.functions.artCollection(0x8FeDec17fB9A312525754B5Ed8Add6c216D90F99)
      
    token_id = st.text_input("enter the token id of the artwork you want to auction")
    if st.button("create auction"):
        creacteAuction = contract.functions.createAuction("token_id")
        
    ###########################################################################       
    ######## DONOR
    #############################################################################
if account == "Donor":
    st.sidebar.radio('Select one:', ['Bitcoin', 'Ethereum', "Dogecoin", "XRP", "Solana"])
    donor_name = st.text_input("Enter Name", value=0, key=0);
    amount = st.text_input("Enter amount you want to donate", value=0, key=1);
    contributor_address = st.text_input("Enter account address", value=0, key=2);
    
    
    if st.button("donate now"):
        donation_hash = contract.functions.doDonation(id, donor_name, amount, address).transact({'from': address, 'gas': 1000000})
        
        st.text('thanks for your donations')
        st.balloons()

    ################################################################################
    ###### Buyer
    ##############################################################################        
if account == "Buyer":
    image1 = Image.open('./images/Fight.jpg')
    image2 = Image.open('./images/Protection.jpg')
    image3 = Image.open('./images/The Ancestors.jpg')
    st.image(image1, caption='Fight')
    st.image(image2, caption='Protection')
    st.image(image3, caption='The Ancestors')

    st.multiselect('pick the art item being auctioned', ['Fight','Protection', 'The Ancestors'])
    
sender = st.text_input('Enter account address')
if st.button("Place bid"):
        bid_hash = second_contract.functions.bid(sender).transact()
        highestBidder = second_contract.functions.highestBidder()
        if highestBidder == sender:
            st.success("Congratulation you won the auction")
            st.balloons()
            








