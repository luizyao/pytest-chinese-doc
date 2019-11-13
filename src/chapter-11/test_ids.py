#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-11-12 13:47:11
-----
Last Modified: 2019-11-12 15:32:19
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


@pytest.mark.parametrize('input, expected', [
    pytest.param(1, 2, id='Windows'),
    pytest.param(3, 4, id='Windows'),
    pytest.param(5, 6, id='Non-Windows')
])
def test_ids_with_ids(input, expected):
    pass
