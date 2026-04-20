"""
ScrollVerse Backend API
========================
A lightweight Flask API that exposes endpoints for the ScrollVerse platform.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    """Return a simple health-check response."""
    return jsonify({"status": "ok", "service": "scrollverse-api"})


# ---------------------------------------------------------------------------
# Token info (static metadata — real data would come from on-chain queries)
# ---------------------------------------------------------------------------

SCROLL_TOKEN = {
    "name": "ScrollToken",
    "symbol": "SCROLL",
    "decimals": 18,
    "max_supply": 1_000_000_000,
    "chain": "Polygon",
}


@app.route("/api/token", methods=["GET"])
def token_info():
    """Return metadata about the $SCROLL token."""
    return jsonify(SCROLL_TOKEN)


# ---------------------------------------------------------------------------
# NFT catalogue (in-memory stub — production would query a contract/IPFS)
# ---------------------------------------------------------------------------

NFT_CATALOGUE = [
    {"token_id": 1, "name": "Scroll #001", "description": "Genesis Guardian NFT", "image": "ipfs://example/1.json"},
    {"token_id": 2, "name": "Scroll #002", "description": "Pioneer Legion NFT",   "image": "ipfs://example/2.json"},
    {"token_id": 3, "name": "Scroll #003", "description": "Council Seat NFT",     "image": "ipfs://example/3.json"},
]


@app.route("/api/nfts", methods=["GET"])
def list_nfts():
    """Return the list of NFTs in the ScrollVerse catalogue."""
    return jsonify(NFT_CATALOGUE)


@app.route("/api/nfts/<int:token_id>", methods=["GET"])
def get_nft(token_id: int):
    """Return a single NFT by token ID."""
    nft = next((n for n in NFT_CATALOGUE if n["token_id"] == token_id), None)
    if nft is None:
        return jsonify({"error": "NFT not found"}), 404
    return jsonify(nft)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import os

    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, host="0.0.0.0", port=5000)
