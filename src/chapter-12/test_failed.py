#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: luizyao (luizyao@163.com)
Created Date: 2019-11-29 15:36:50
-----
Modified: 2019-11-29 17:12:27
Modified By: luizyao (luizyao@163.com)
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


@pytest.mark.parametrize('num', [1, 2])
def test_failed(num):
    assert num == 1
