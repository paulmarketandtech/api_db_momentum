import pytest
from fastapi.testclient import TestClient

os.environ["DATABASE_PATH"] = "api_db_momentum/tests/fixtures/test_data.db"
from ..main import app


@pytest.fixture
def client():
    return TestClient(app)
