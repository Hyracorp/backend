import pytest

pytestmark = pytest.mark.django_db


def test_example(self, user_factory):
    # Arrage - bring in resource
    # Act - perform action
    x = user_factory()
    # Assert -  check if outcome is expected
    assert x.__str__() == "my test data"
