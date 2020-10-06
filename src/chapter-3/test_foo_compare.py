class Foo:
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val

    def __repr__(self):
        return str(self.val)


def test_foo_compare():
    f1 = Foo(1)
    f2 = Foo(2)
    assert f1 == f2
