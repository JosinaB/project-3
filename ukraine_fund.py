# Ukraine Fund Marketplace Frontend

# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List




# From ukraine_donation_wallet.py import w3, generate_account, get_balance

from ukraine_donation_wallet import w3, generate_account, get_balance

################################################################################
# ArtWorks Database 


artworks_database = {
    "Avatar": ["Avatar", xx],
    "Brotherly_Arms": ["Brotherly_Arms", xx],
    "Beauty_Comes_from_the_Heart": ["Beauty_Comes_from_the_Heart", xx],
    "Help_your_people": ["Help_your_people", xx],
    
}

# List of the Artworks by name
artworks = ["Avatar", "Brotherly_Arms", "Beauty_Comes_from_the_Heart", "Help_your_people"]

# get_artworks function to display the purchase information from the art pieces
def get_artworks():
    """Display the database of artworks to purchase information."""
    db_list = list(artworks_database.values())

    for number in range(len(artworks)):
        st.write("Name: ", db_list[number][0])
        st.write("Price in Ether: ", db_list[number][1], "eth")
        st.text(" \n")

################################################################################
# Streamlit Code

# Create Streamlit application headings using `st.markdown` to explain this app is for buying artworks whose proceeds feed the Ukraine Fund
st.markdown("# Artworks for Ukraine")
st.markdown("## Donate to the Ukraine Fund by purchasing an art piece!")
st.text(" \n")

#  Call the `generate_account` function and save it as the variable `account`
account = generate_account()

#  Call the `get_balance` function and save it as the variable `ether`
ether = get_balance(account.address)

# Disply the balance of ether in the account
st.sidebar.markdown("## Your Balance of Ether")
st.sidebar.markdown(ether)
st.sidebar.markdown("---------")

# Create a select box to chose a art piece using `st.sidebar.selectbox`
artworks = st.sidebar.selectbox('Select an art piece', artworks)

#  Create a header using ` st.sidebar.markdown()` to display art piece name and price.
st.sidebar.markdown("## Art Piece Name and Price")

# Identify the art piece for purchase by name
artworks = art_database[artworks][0]

# Create a variable called `artworks_price` to retrive the art pieces prices from the `artworks_database` using block notation.
artworks_price = art_database[artworks][1]

# Use a conditional statement using the `if` keyword to check if the selected art piece can be purchased. This will be done by checking the user's account balance that wishes to make the purchase.
if artworks_price <= ether:
  new_balance = float(ether) - float(artworks_price)
# Write the art piece name to the sidebar
  st.sidebar.write("If you buy", artworks, "for", artworks_price, "eth, your account balance will be", new_balance, ".")
  get_artworks()
else:
  st.sidebar.write("With a balance of", ether, "ether, you can't buy", artworks, "for", artworks_price, "eth." )
  get_artworks()
