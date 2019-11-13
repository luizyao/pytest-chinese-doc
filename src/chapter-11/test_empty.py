#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-11-12 16:54:36
-----
Last Modified: 2019-11-12 17:00:41
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


def read_value():
    if sys.version_info >= (3, 8):
        return [1, 2, 3]
    else:
        return []


@pytest.mark.parametrize('test_input', read_value())
def test_empty(test_input):
    assert test_input
