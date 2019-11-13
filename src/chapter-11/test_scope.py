#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-11-12 15:48:08
-----
Last Modified: 2019-11-13 13:24:51
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


@pytest.fixture(scope='module')
def test_input(request):
    pass


@pytest.fixture(scope='module')
def expected(request):
    pass


@pytest.mark.parametrize('test_input, expected', [(1, 2), (3, 4)],
                         indirect=True)
def test_scope1(test_input, expected):
    pass


@pytest.mark.parametrize('test_input, expected', [(1, 2), (3, 4)],
                         indirect=True)
def test_scope2(test_input, expected):
    pass
