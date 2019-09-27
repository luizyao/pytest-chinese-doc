#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-09-28 6:41:25
-----
Last Modified: 2019-09-28 6:41:37
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


def test_set_comparison():
    set1 = set('1308')
    set2 = set('8035')
    assert set1 == set2


def test_long_str_comparison():
    str1 = 'show me codes'
    str2 = 'show me money'
    assert str1 == str2


def test_dict_comparison():
    dict1 = {
        'x': 1,
        'y': 2,
    }
    dict2 = {
        'x': 1,
        'y': 1,
    }
    assert dict1 == dict2
