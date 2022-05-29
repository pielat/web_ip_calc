from web_ip_calc.functions import check_class

def test_check_class() -> str:
    assert check_class("191.255.255.254") == "This is class B."
