#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-09-20 22:33:38
-----
Last Modified: 2019-09-25 16:13:28
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


def test_ehlo(smtp_connection):
    response, _ = smtp_connection.ehlo()
    assert response == 250
    smtp_connection.extra_attr = 'test'
    assert 0  # 为了展示，强制置为失败


def test_noop(smtp_connection):
    response, _ = smtp_connection.noop()
    assert response == 250
    assert smtp_connection.extra_attr == 0
