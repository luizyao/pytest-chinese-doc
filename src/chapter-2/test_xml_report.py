import pytest


@pytest.mark.test_id(10086)
def test_marker_test_id():
    pass


def test_record_property(record_property):
    record_property("test_id", 10010)


def test_record_xml_attribute(record_xml_attribute):
    record_xml_attribute("test_id", 10010)
    record_xml_attribute("classname", "custom_classname")


@pytest.fixture(scope="session")
def log_global_env_facts(record_testsuite_property):
    record_testsuite_property("EXECUTOR", "luizyao")
    record_testsuite_property("LOCATION", "NJ")


def test_testsuite_property(log_global_env_facts):
    pass
