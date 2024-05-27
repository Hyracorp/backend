# from pytest_factoryboy import register

# from .factories import UserFactory

# register(UserFactory)

# fixtures

from rest_framework.test import APIClient
import pytest


@pytest.fixture
def api_client():
    return APIClient()
