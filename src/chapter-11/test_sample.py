#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-11-11 16:07:30
-----
Last Modified: 2019-11-12 11:05:06
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

from _pytest.mark.structures import ParameterSet


@pytest.mark.parametrize(
    'input, expected',
    [(1, 2), ParameterSet(values=(1, 2), marks=[], id=None)])
def test_sample(input, expected):
    assert input + 1 == expected
