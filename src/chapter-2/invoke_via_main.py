#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-09-27 16:33:39
-----
Last Modified: 2019-09-27 17:18:26
Modified By: Luiz Yao (luizyao@163.com)
-----
THIS PROGRAM IS FREE SOFTWARE, IS LICENSED UNDER MIT.

A short and simple permissive license with conditions
only requiring preservation of copyright and license notices.

Copyright © 2019 Yao Meng
-----
HISTORY:
Date      		By      		Comments
----------		--------		---------------------------------------------------------
'''

import time


def test_one():
    time.sleep(10)


if __name__ == '__main__':
    import pytest
    ret = pytest.main(['-q', __file__])
    print("pytest.main() 返回 pytest.ExitCode.INTERRUPTED：", ret == pytest.ExitCode.INTERRUPTED)
