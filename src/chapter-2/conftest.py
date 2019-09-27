#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-09-27 15:13:44
-----
Last Modified: 2019-09-27 15:13:46
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


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        for marker in item.iter_markers(name="test_id"):
            test_id = marker.args[0]
            item.user_properties.append(("test_id", test_id))
