#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-10-23 13:53:28
-----
Last Modified: 2019-10-23 14:18:41
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

CONTENT = "content"


def test_create_file(tmp_path):
    d = tmp_path / "sub"  
    d.mkdir()  # 创建一个子目录
    p = d / "hello.txt"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT
    assert len(list(tmp_path.iterdir())) == 1  # iterdir() 迭代目录，返回迭代器
    assert 0  # 为了展示，强制置为失败
