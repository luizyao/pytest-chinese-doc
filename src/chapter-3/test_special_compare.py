def test_set_comparison():
    set1 = set("1308")
    set2 = set("8035")
    assert set1 == set2


def test_long_str_comparison():
    str1 = "show me codes"
    str2 = "show me money"
    assert str1 == str2


def test_dict_comparison():
    dict1 = {
        "x": 1,
        "y": 2,
    }
    dict2 = {
        "x": 1,
        "y": 1,
    }
    assert dict1 == dict2
