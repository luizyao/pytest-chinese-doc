#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-11-05 16:35:41
-----
Last Modified: 2019-11-05 17:36:43
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

pytestmark = pytest.mark.skip('作用于模块中的每一个用例，所以 pytest 共收集到两个 SKIPPED 的用例。')

# pytest.skip('在用例收集阶段就已经跳出了，所以不会收集到任何用例。', allow_module_level=True)


def test_one():
    assert True


def test_two():
    assert True
