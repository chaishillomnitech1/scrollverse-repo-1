'use strict';

/**
 * ScrollVerse Frontend Application
 *
 * Handles wallet connection (MetaMask / EIP-1193) and renders
 * placeholder NFT cards for demonstration purposes.
 */

const NETWORK = {
  chainId: '0x89',          // Polygon Mainnet
  chainName: 'Polygon',
  nativeCurrency: { name: 'MATIC', symbol: 'MATIC', decimals: 18 },
  rpcUrls: ['https://polygon-rpc.com/'],
  blockExplorerUrls: ['https://polygonscan.com/'],
};

/** Update the wallet status text element. */
function setWalletStatus(message) {
  const el = document.getElementById('wallet-status');
  if (el) el.textContent = message;
}

/** Shorten a hex address for display (e.g. 0x1234…abcd). */
function shortenAddress(address) {
  return `${address.slice(0, 6)}…${address.slice(-4)}`;
}

/** Ask MetaMask to switch to (or add) the target network. */
async function switchToNetwork() {
  try {
    await window.ethereum.request({
      method: 'wallet_switchEthereumChain',
      params: [{ chainId: NETWORK.chainId }],
    });
  } catch (err) {
    if (err.code === 4902) {
      await window.ethereum.request({
        method: 'wallet_addEthereumChain',
        params: [NETWORK],
      });
    } else {
      throw err;
    }
  }
}

/** Connect to the user's injected wallet (MetaMask / EIP-1193). */
async function connectWallet() {
  if (typeof window.ethereum === 'undefined') {
    setWalletStatus('MetaMask is not installed. Please install it from metamask.io.');
    return;
  }

  try {
    const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
    if (accounts.length === 0) {
      setWalletStatus('No accounts found. Please unlock MetaMask.');
      return;
    }
    await switchToNetwork();
    setWalletStatus(`Connected: ${shortenAddress(accounts[0])}`);
  } catch (err) {
    setWalletStatus(`Connection failed: ${err.message}`);
  }
}

/** Render sample NFT cards in the #nft-grid element. */
function renderNFTGrid() {
  const grid = document.getElementById('nft-grid');
  if (!grid) return;

  const placeholders = [
    { id: 1, name: 'Scroll #001', description: 'Genesis Guardian NFT' },
    { id: 2, name: 'Scroll #002', description: 'Pioneer Legion NFT' },
    { id: 3, name: 'Scroll #003', description: 'Council Seat NFT' },
  ];

  placeholders.forEach(({ id, name, description }) => {
    const card = document.createElement('div');
    card.className = 'nft-card';
    card.innerHTML = `
      <strong>${name}</strong>
      <p>${description}</p>
      <p style="font-size:0.8rem;margin-top:0.5rem;color:#555;">Token ID: ${id}</p>
    `;
    grid.appendChild(card);
  });
}

/** Bootstrap the application once the DOM is ready. */
function init() {
  renderNFTGrid();

  const connectBtn = document.getElementById('connect-wallet-btn');
  if (connectBtn) {
    connectBtn.addEventListener('click', connectWallet);
  }

  const headerBtn = document.getElementById('connect-btn');
  if (headerBtn) {
    headerBtn.addEventListener('click', (e) => {
      e.preventDefault();
      connectWallet();
    });
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
