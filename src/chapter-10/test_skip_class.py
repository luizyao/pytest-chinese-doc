#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-11-05 16:17:52
-----
Last Modified: 2019-11-05 16:33:22
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


@pytest.mark.skip("作用于类中的每一个用例，所以 pytest 共收集到两个 SKIPPED 的用例。")
class TestMyClass():
    def test_one(self):
        assert True

    def test_two(self):
        assert True
