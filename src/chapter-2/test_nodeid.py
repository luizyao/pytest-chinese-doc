import pytest


def test_one():
    pass


class TestNodeid:
    def test_one(self):
        pass

    @pytest.mark.parametrize("x,y", [(1, 2), (3, 4)])
    def test_two(self, x, y):
        assert x + 1 == y
