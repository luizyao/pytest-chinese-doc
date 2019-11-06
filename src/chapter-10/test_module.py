#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-11-05 14:43:53
-----
Last Modified: 2019-11-05 16:17:16
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

import sys

import pytest

minversion = pytest.mark.skipif(sys.version_info < (3, 8),
                                reason='请使用 python 3.8 或者更高的版本。')


@minversion
def test_one():
    assert True
