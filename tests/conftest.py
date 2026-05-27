from copy import deepcopy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    with TestClient(app_module.app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    """Snapshot and restore the module-level `activities` dict around each test.

    This ensures test isolation because `src.app.activities` is mutated by
    the endpoints under test.
    """
    snapshot = deepcopy(app_module.activities)
    try:
        yield
    finally:
        app_module.activities.clear()
        app_module.activities.update(snapshot)
