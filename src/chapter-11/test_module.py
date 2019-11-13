#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-11-13 9:14:57
-----
Last Modified: 2019-11-13 9:20:27
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

pytestmark = pytest.mark.parametrize('test_input, expected', [(1, 2), (3, 4)])


def test_module(test_input, expected):
    assert test_input + 1 == expected
