#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-09-26 9:50:34
-----
Last Modified: 2019-09-26 14:05:40
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

import smtplib

import pytest


def determine_scope(fixture_name: str, config: object) -> str:
    if config.getoption('--keep-connection'):
        return 'module'
    return 'function'


@pytest.fixture(scope=determine_scope)
def dynamic_smtp_connection():
    return smtplib.SMTP("smtp.163.com", 25, timeout=5)


def test_ehlo(dynamic_smtp_connection):
    response, _ = dynamic_smtp_connection.ehlo()
    assert response == 250
    assert 0  # 为了展示，强制置为失败


def test_noop(dynamic_smtp_connection):
    response, _ = dynamic_smtp_connection.noop()
    assert response == 250
    assert 0  # 为了展示，强制置为失败
