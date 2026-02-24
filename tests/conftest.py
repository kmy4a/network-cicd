import pytest
from yaml import safe_load


@pytest.fixture
def fabric():
    with open("desired_state.yml") as f:
        return safe_load(f)
