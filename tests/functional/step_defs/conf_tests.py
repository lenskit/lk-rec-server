import pytest

@pytest.fixture(scope="session", autouse=True)
def setup_for_all_tests():
    pass