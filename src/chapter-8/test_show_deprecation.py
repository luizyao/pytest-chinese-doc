#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-10-30 17:46:41
-----
Last Modified: 2019-10-31 15:40:30
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

import warnings
import pytest


def api_call_v1():
    warnings.warn('v1版本已废弃，请使用v2版本的api；', DeprecationWarning)
    return 200


def test_deprecation():
    assert pytest.deprecated_call(api_call_v1) == 200
