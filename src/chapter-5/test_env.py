#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-10-18 13:53:11
-----
Last Modified: 2019-10-18 14:03:21
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

import os

import pytest


def get_os_user():
    username = os.getenv('USER')

    if username is None:
        raise IOError('"USER" environment variable is not set.')

    return username


def test_user(monkeypatch):
    monkeypatch.setenv('USER', 'luizyao')
    assert get_os_user() == 'luizyao'


def test_raise_exception(monkeypatch):
    monkeypatch.delenv('USER', raising=False)
    pytest.raises(IOError, get_os_user)
