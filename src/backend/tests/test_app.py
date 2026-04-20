"""
Tests for the ScrollVerse backend API.
"""

import pytest
from src.backend.app import app as flask_app


@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------------------------

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "scrollverse-api"


# ---------------------------------------------------------------------------
# Token endpoint
# ---------------------------------------------------------------------------

def test_token_info(client):
    resp = client.get("/api/token")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["symbol"] == "SCROLL"
    assert data["decimals"] == 18
    assert data["max_supply"] == 1_000_000_000


# ---------------------------------------------------------------------------
# NFT endpoints
# ---------------------------------------------------------------------------

def test_list_nfts(client):
    resp = client.get("/api/nfts")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_get_nft_found(client):
    resp = client.get("/api/nfts/1")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["token_id"] == 1
    assert "name" in data


def test_get_nft_not_found(client):
    resp = client.get("/api/nfts/9999")
    assert resp.status_code == 404
    data = resp.get_json()
    assert "error" in data
