pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "./UkraineAuction.sol";

contract UkraineArtMarket is ERC1155 {
    uint public Art = 0;
    uint public Token = 1;
    

    constructor() public ERC1155("link{id.json}"){
    _mint(msg.sender, Art, 1, "");
    _mint(msg.sender) Token 10**18, "");  

    }}

    address payable foundation_address = 0x155bDbB005dBd6987707544aA11d586C1C072d10;

    mapping(uint => UkrainAuction) public auctions;

    modifier ArtRegistered(uint token_id) {
        require(_exists(token_id), "Art not registered!");
        _;
    }

    function registerArt(string memory uri) public payable onlyOwner {
        token_ids.increment();
        uint token_id = token_ids.current();
        _mint(foundation_address, token_id);
        _setTokenURI(token_id, uri);
        createAuction(token_id);
    }

    function createAuction(uint token_id) public onlyOwner {
        auctions[token_id] = new UkraineArtAuction(foundation_address);
    }

    function endAuction(uint token_id) public onlyOwner landRegistered(token_id) {
        MartianAuction auction = auctions[token_id];
        auction.auctionEnd();
        safeTransferFrom(owner(), auction.highestBidder(), token_id);
    }

    function auctionEnded(uint token_id) public view returns(bool) {
        UkrainAuction auction = auctions[token_id];
        return auction.ended();
    }

    function highestBid(uint token_id) public view landRegistered(token_id) returns(uint) {
        UkraineArtAuction auction = auctions[token_id];
        return auction.highestBid();
    }

    function pendingReturn(uint token_id, address sender) public view ArtRegistered(token_id) returns(uint) {
        UkraineAuction auction = auctions[token_id];
        return auction.pendingReturn(sender);
    }

    function bid(uint token_id) public payable ArtRegistered(token_id) {
        UkraineAuction auction = auctions[token_id];
        auction.bid.value(msg.value)(msg.sender);
    }

}
