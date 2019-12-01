#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: luizyao (luizyao@163.com)
Created Date: 2019-11-30 20:35:07
-----
Modified: 2019-11-30 20:36:29
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

# content of test_caching.py
import pytest


def expensive_computation():
    print("running expensive computation...")


@pytest.fixture
def mydata(request):
    # 从缓存中读取数据
    val = request.config.cache.get("example/value", None)
    if val is None:
        expensive_computation()
        val = 42
        # 如果缓存中没有，设置缓存中的值
        request.config.cache.set("example/value", val)
    return val


def test_function(mydata):
    assert mydata == 23
