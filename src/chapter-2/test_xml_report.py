#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
Author: Luiz Yao (luizyao@163.com)
Created Date: 2019-09-27 14:44:24
-----
Last Modified: 2019-09-27 16:18:35
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

import pytest


@pytest.fixture(scope="session")
def log_global_env_facts(record_testsuite_property):
    record_testsuite_property("EXECUTOR", "luizyao")
    record_testsuite_property("LOCATION", "NJ")


def test_record_property(record_property):
    record_property("test_id", 10010)
    assert 1


@pytest.mark.test_id(10010)
def test_record_property1():
    assert 1


def test_record_property2(record_xml_attribute):
    record_xml_attribute('test_id', 10010)
    record_xml_attribute('classname', 'custom_classname')
    assert 1


def test_record_property3(log_global_env_facts):
    assert 1
