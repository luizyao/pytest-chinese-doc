#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-10-10 16:08:12
-----
Last Modified: 2019-10-10 16:12:09
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

from pathlib import Path


def getssh():
    return Path.home() / ".ssh"


def test_getssh(monkeypatch):
    def mockreturn():
        return Path("/abc")

    # 替换 Path.home
    # 需要在真正的调用之前执行
    monkeypatch.setattr(Path, "home", mockreturn)
    
    # 将会使用 mockreturn 代替 Path.home
    x = getssh()
    assert x == Path("/abc/.ssh")
