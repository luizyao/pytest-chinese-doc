#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-09-19 5:35:12
-----
Last Modified: 2019-10-07 8:27:16
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
import smtplib
import tempfile

import pytest


@pytest.fixture(scope='module')
def smtp_connection():
    return smtplib.SMTP("smtp.163.com", 25, timeout=5)


@pytest.fixture(scope='package')
def smtp_connection_package():
    return smtplib.SMTP("smtp.163.com", 25, timeout=5)


@pytest.fixture()
def smtp_connection_yield():
    smtp_connection = smtplib.SMTP("smtp.163.com", 25, timeout=5)
    yield smtp_connection
    print("关闭SMTP连接")
    smtp_connection.close()


@pytest.fixture(scope='module')
def smtp_connection_request(request):
    server, port = getattr(request.module, 'smtp_server', ("smtp.163.com", 25))
    with smtplib.SMTP(server, port, timeout=5) as smtp_connection:
        yield smtp_connection
        print("断开 %s：%d" % (server, port))


@pytest.fixture(scope='module', params=['smtp.163.com', 'smtp.126.com'])
def smtp_connection_params(request):
    server = request.param
    with smtplib.SMTP(server, 25, timeout=5) as smtp_connection:
        yield smtp_connection
        print("断开 %s：%d" % (server, 25))


@pytest.fixture()
def cleandir():
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
