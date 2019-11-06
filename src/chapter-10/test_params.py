#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-11-06 9:40:57
-----
Last Modified: 2019-11-06 15:51:55
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

import pytest
import sys


@pytest.mark.parametrize(
    ('n', 'expected'),
    [(2, 1),
     pytest.param(2, 1, marks=pytest.mark.xfail(), id='XPASS'),
     pytest.param(0, 1, marks=pytest.mark.xfail(raises=ZeroDivisionError), id='XFAIL'),
     pytest.param(1, 2, marks=pytest.mark.skip(reason='无效的参数，跳过执行')),
     pytest.param(1, 2, marks=pytest.mark.skipif(sys.version_info <= (3, 8), reason='请使用3.8及以上版本的python。'))])
def test_params(n, expected):
    assert 2 / n == expected
