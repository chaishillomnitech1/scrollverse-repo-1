// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// @title ScrollNFT
/// @notice ERC-721 NFT collection for the ScrollVerse platform.
contract ScrollNFT is ERC721URIStorage, Ownable {
    uint256 private _nextTokenId;

    constructor(address initialOwner)
        ERC721("ScrollVerse NFTs", "SVNFT")
        Ownable(initialOwner)
    {}

    /// @notice Mint a new NFT. Only callable by the contract owner.
    /// @param to       Recipient address.
    /// @param tokenURI Metadata URI for the token.
    /// @return tokenId The ID of the newly minted token.
    function mint(address to, string calldata tokenURI)
        external
        onlyOwner
        returns (uint256 tokenId)
    {
        tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, tokenURI);
    }
}
