#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-11-04 16:25:07
-----
Last Modified: 2019-11-04 17:16:01
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


def str_bytes():
    '''返回字节编码

    >>> str_bytes()  # doctest: +ALLOW_BYTES
    'bytes' 
    ''' 
    return b'bytes'


def number():
    '''浮点数的精度

    >>> import math
    >>> math.pi  # doctest: +NUMBER
    3.14 
    '''
    return 1


def str_number():
    '''浮点数字符串的精度

    >>> str_number()  # doctest: +NUMBER
    '3.14' 
    '''
    return '3.1415'
