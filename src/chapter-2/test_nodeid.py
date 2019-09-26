#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-09-27 6:38:24
-----
Last Modified: 2019-09-27 6:41:12
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


def test_one():
    print('test_one')
    assert 1


class TestNodeId:
    def test_one(self):
        print('TestNodeId::test_one')
        assert 1

    @pytest.mark.parametrize('x,y', [(1, 1), (3, 4)])
    def test_two(self, x, y):
        print(f'TestNodeId::test_two::{x} == {y}')
        assert x == y
