#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-10-10 17:03:27
-----
Last Modified: 2019-10-14 16:39:42
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

from urllib import request

import pytest

from app import get


# 自定义的类模拟 urlopen 的返回值
class MockResponse:

    # 永远返回一个固定的 bytes 类型的数据
    @staticmethod
    def read():
        return b'luizyao.com'


def test_get(monkeypatch):
    def mock_urlopen(*args, **kwargs):
        return MockResponse()

    # 使用 request.mock_urlopen 代替 request.urlopen
    monkeypatch.setattr(request, 'urlopen', mock_urlopen)

    data = get('https://luizyao.com')
    assert data == 'luizyao.com'


# monkeypatch 是 function 级别作用域的，所以 mock_response 也只能是 function 级别，
# 否则会报 ScopeMismatch: You tried to access the 'function' scoped fixture 'monkeypatch' with a 'module' scoped request object
@pytest.fixture
def mock_response(monkeypatch):
    def mock_urlopen(*args, **kwargs):
        return MockResponse()

    # 使用 request.mock_urlopen 代替 request.urlopen
    monkeypatch.setattr(request, 'urlopen', mock_urlopen)


# 使用 mock_response 代替原先的 monkeypatch
def test_get_fixture1(mock_response):
    data = get('https://luizyao.com')
    assert data == 'luizyao.com'


# 使用 mock_response 代替原先的 monkeypatch
def test_get_fixture2(mock_response):
    data = get('https://bing.com')
    assert data == 'luizyao.com'


@pytest.fixture
def no_request(monkeypatch):
    monkeypatch.delattr('urllib.request.urlopen')


def test_delattr(no_request):
    data = get('https://bing.com')
    assert data == 'luizyao.com'
