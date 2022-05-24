// contracts/GameItems.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC1155/ERC1155.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/access/Ownable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/Counters.sol";
import "./UkraineAuction.sol";

contract UkraineNFT is ERC1155, Ownable {
    
    uint256 public constant ArtToken = 0;
    uint256 public constant ArtPiece = 1;
  
    constructor() public ERC1155("https://ipfs.io/ipfs/Qmag2VFDcHXSyvXAiAt8reBMn9gi1Skx6zVpvvmuSevVLr?filename=bensound-littleidea.mp3") {
        _mint(msg.sender, ArtToken, 100*10, "");
        _mint(msg.sender, ArtPiece, 5, "");
        }
        using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    mapping(uint256 => string) private _tokenURIs;
    address payable foundation_address = msg.sender;
    mapping(uint => UkraineAuction) public auctions;
    //modifier ArtRegistered(uint token_id) {
      //  require(_exists(token_id), "Art not registered!");
        //_;
    }
    function registerArt(string memory uri) public payable onlyOwner {
        tokenIds.increment();
        uint token_id = tokenIds.current();
        _mint(foundation_address, token_id);
        _setTokenURI(token_id, uri);
        createAuction(token_id);
    }
      function createAuction(uint token_id) public onlyOwner {
        auctions[token_id] = new UkraineAuction(foundation_address);
    }
    function endAuction(uint token_id) public onlyOwner ArtRegistered(token_id) {
        UkraineAuction auction = auctions[token_id];
        auction.auctionEnd();
        safeTransferFrom(owner(), auction.highestBidder(), token_id);
    }
    function auctionEnded(uint token_id) public view returns(bool) {
        UkraineAuction auction = auctions[token_id];
        return auction.ended();
    }
    function highestBid(uint token_id) public view ArtRegistered(token_id) returns(uint) {
        UkraineAuction auction = auctions[token_id];
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
