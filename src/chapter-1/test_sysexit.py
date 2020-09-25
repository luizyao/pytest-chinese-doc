import pytest


def f():
    # 请求退出解释器
    raise SystemExit(1)


def test_mytest():
    with pytest.raises(SystemExit):
        f()
