#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-11-12 11:19:37
-----
Last Modified: 2019-11-12 13:38:34
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


@pytest.fixture()
def max(request):
    return request.param - 1


@pytest.fixture()
def min(request):
    return request.param + 1


# 默认 indirect 为 False
@pytest.mark.parametrize('min, max', [(1, 2), (3, 4)])
def test_indirect(min, max):
    assert min <= max


# min max 对应的实参重定向到同名的 fixture 中
@pytest.mark.parametrize('min, max', [(1, 2), (3, 4)], indirect=True)
def test_indirect_indirect(min, max):
    assert min >= max


# 只将 max 对应的实参重定向到 fixture 中
@pytest.mark.parametrize('min, max', [(1, 2), (3, 4)], indirect=['max'])
def test_indirect_part_indirect(min, max):
    assert min == max
