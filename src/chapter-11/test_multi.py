#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-11-12 17:18:53
-----
Last Modified: 2019-11-12 18:05:13
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


@pytest.mark.parametrize('test_input', [1, 2, 3])
@pytest.mark.parametrize('test_output, expected', [(1, 2), (3, 4)])
def test_multi(test_input, test_output, expected):
    pass
