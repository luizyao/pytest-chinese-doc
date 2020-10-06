import time


def test_one():
    time.sleep(10)


if __name__ == "__main__":
    import pytest

    ret = pytest.main(["-q", __file__])
    print(
        "pytest.main() 返回 pytest.ExitCode.INTERRUPTED：",
        ret == pytest.ExitCode.INTERRUPTED,
    )
