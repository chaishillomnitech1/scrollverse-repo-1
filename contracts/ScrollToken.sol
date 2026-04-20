// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// @title ScrollToken
/// @notice ERC-20 governance token for the ScrollVerse platform.
contract ScrollToken is ERC20, Ownable {
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10 ** 18; // 1 billion tokens

    constructor(address initialOwner)
        ERC20("ScrollToken", "SCROLL")
        Ownable(initialOwner)
    {}

    /// @notice Mint new tokens. Only callable by the contract owner.
    /// @param to      Recipient address.
    /// @param amount  Amount of tokens to mint (in wei).
    function mint(address to, uint256 amount) external onlyOwner {
        require(totalSupply() + amount <= MAX_SUPPLY, "ScrollToken: max supply exceeded");
        _mint(to, amount);
    }
}
