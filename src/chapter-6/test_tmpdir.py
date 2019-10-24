#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-10-24 14:23:40
-----
Last Modified: 2019-10-24 14:26:16
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


def test_create_file(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")  # 创建子文件夹，并新建文件
    p.write(CONTENT)
    assert p.read() == CONTENT
    assert len(tmpdir.listdir()) == 1  # iterdir() 迭代目录，返回列表
    assert 0  # 为了展示，强制置为失败
