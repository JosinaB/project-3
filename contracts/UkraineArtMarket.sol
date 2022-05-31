pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/ownership/Ownable.sol";
import "./UkraineAuction.sol";

contract UkraineArtMarket is ERC721Full, Ownable {

    constructor() ERC721Full("UkraineArtMarket", "ART") public {}
      struct Artwork {
        string name;
        string artist;
        uint256 appraisalValue;
    }
        struct Contributors {
        uint id;
        string name;
        uint256 amount;
        address sender_address;
    }

    using Counters for Counters.Counter;

    Counters.Counter token_ids;

    address payable foundation_address = msg.sender;

    uint256 id = 0;
    mapping(uint => Contributors) public contributor;
    mapping(uint => UkraineAuction) public auctions;
    mapping(uint256 => Artwork) public artCollection;
    modifier artRegistered(uint token_id) {
        require(_exists(token_id), "Art not registered!");
        _;
    }

     function registerArtwork(
        address owner,
        string memory name,
        string memory artist,
        uint256 initialAppraisalValue,
        string memory tokenURI
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();

        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);

        artCollection[tokenId] = Artwork(name, artist, initialAppraisalValue);

        return tokenId;
    }
    function createAuction(uint token_id) public onlyOwner {
        auctions[token_id] = new UkraineAuction(foundation_address);
    }

    function endAuction(uint token_id) public onlyOwner artRegistered(token_id) {
        UkraineAuction auction = auctions[token_id];
        auction.auctionEnd();
        safeTransferFrom(owner(), auction.highestBidder(), token_id);
    }

    function auctionEnded(uint token_id) public view returns(bool) {
        UkraineAuction auction = auctions[token_id];
        return auction.ended();
    }

    function highestBid(uint token_id) public view artRegistered(token_id) returns(uint) {
        UkraineAuction auction = auctions[token_id];
        return auction.highestBid();
    }

    function pendingReturn(uint token_id, address sender) public view artRegistered(token_id) returns(uint) {
        UkraineAuction auction = auctions[token_id];
        return auction.pendingReturn(sender);
    }

    function bid(uint token_id) public payable artRegistered(token_id) {
        UkraineAuction auction = auctions[token_id];
        auction.bid.value(msg.value)(msg.sender);
    }

       function doDonation(string memory name) public payable {
        id += 1;
        contributor[id] = Contributors(id, name, msg.value, msg.sender);
    }


    function getBalance() public view returns(uint) {
        return address(this).balance;
    }

    function withdrawMoney(address payable _to) public onlyOwner {
        _to.transfer(getBalance());
    }

}