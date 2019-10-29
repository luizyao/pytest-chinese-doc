#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-10-29 14:33:34
-----
Last Modified: 2019-10-29 16:18:26
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

import sys


def test_output(capsys):
    print('hello')
    print('world', file=sys.stderr, end='&')  # 标准错误输出，修改结束符
    captured = capsys.readouterr()
    assert captured.out == 'hello\n'  # print() 默认的结束符是换行符
    assert captured.err == 'world&'
    print('next')
    captured = capsys.readouterr()
    assert captured.out == 'next\n'


def test_binary_output(capsysbinary):
    print('hello')
    captured = capsysbinary.readouterr()
    assert captured.out == b'hello\n'


def test_disabling_capturing(capsys):
    print("hello")
    with capsys.disabled():
        print("world")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"
