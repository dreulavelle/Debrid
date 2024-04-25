import pytest
from debrid.realdebrid import RealDebrid


with open(".env") as f:
    API_KEY = f.readline().strip()

if not API_KEY:
    raise ValueError("API key not found in .env file")

@pytest.fixture
def rd():
    return RealDebrid(API_KEY)

def test_valid_instantiation(rd):
    assert isinstance(rd, object)

def test_is_downloaded(rd):
    assert isinstance(rd.is_downloaded("24e76cf367808b29d2b88c3b4dce07a3b605e42e"), bool)

def test_get_torrents(rd):
    assert isinstance(rd.get_torrents(), list)

def test_is_cached(rd):
    assert isinstance(rd.is_cached(["24e76cf367808b29d2b88c3b4dce07a3b605e42e"]), dict)
