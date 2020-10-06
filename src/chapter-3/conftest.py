from test_foo_compare import Foo


def pytest_assertrepr_compare(op, left, right):
    if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
        return [
            "比较两个Foo实例:",  # 顶头写概要
            "   值: {} != {}".format(left.val, right.val),  # 除了第一个行，其余都可以缩进
        ]
