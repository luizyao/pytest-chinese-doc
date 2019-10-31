#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-10-30 11:25:43
-----
Last Modified: 2019-10-30 16:49:56
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

import warnings
import pytest


def api_v1():
    warnings.warn(UserWarning('请使用新版本的API。'))
    return 1


def test_one():
    assert api_v1() == 1


@pytest.mark.filterwarnings('ignore::UserWarning')
def test_two():
    assert api_v1() == 1
