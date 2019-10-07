#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-10-06 13:12:47
-----
Last Modified: 2019-10-06 13:43:35
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


@pytest.fixture(params=[('3+5', 8),
                        pytest.param(('6*9', 42),
                                     marks=pytest.mark.xfail,
                                     id='failed')])
def data_set(request):
    return request.param


def test_data(data_set):
    assert eval(data_set[0]) == data_set[1]


@pytest.mark.parametrize(
    'test_input, expected',
    [('3+5', 8),
     pytest.param('6*9', 42, marks=pytest.mark.xfail, id='failed')])
def test_data2(test_input, expected):
    assert eval(test_input) == expected
