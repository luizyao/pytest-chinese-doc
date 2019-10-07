#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-10-04 7:05:16
-----
Last Modified: 2019-10-04 7:29:59
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


@pytest.fixture(params=[0, 1], ids=['spam', 'ham'])
def a(request):
    return request.param


def test_a(a):
    pass


def idfn(fixture_value):
    if fixture_value == 0:
        return "eggs"
    elif fixture_value == 1:
        return False
    elif fixture_value == 2:
        return None
    else:
        return fixture_value


@pytest.fixture(params=[0, 1, 2, 3], ids=idfn)
def b(request):
    return request.param


def test_b(b):
    pass


class C:
    pass


@pytest.fixture(params=[(1, 2), {'d': 1}, C()])
def c(request):
    return request.param


def test_c(c):
    pass
