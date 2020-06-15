import pytest


class TestClass(object):
    # Define what ansible tests to execute on.
    pytestmark = [
        pytest.mark.example
        ]
    def test_helloworld(self):
        pass
