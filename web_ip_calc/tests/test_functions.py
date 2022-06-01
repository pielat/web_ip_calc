from web_ip_calc.functions import check_class, calculate_cidr


def test_check_class():
    assert check_class("191.255.255.254") == "This is class B."
    assert check_class("192.0.0.1") == "This is class C."
    assert check_class("1.0.0.1") == "This is class A."
    assert check_class("248.0.0.1") == "This is class F."
    assert check_class("247.255.255.255") == "This is class E."


def test_calculate_cidr():
    assert calculate_cidr("11111111.11111111.11111111.00000000") == 24
    assert calculate_cidr("11111111.11111111.00000000.00000000") == 16
    assert calculate_cidr("11111111.11111111.11111111.11111100") == 30
    assert calculate_cidr("11111111.00000000.00000000.00000000") == 8
