from share.types import Result, Ok, Err

import pytest


def test_result_match_ok():
    a: Result[int] = Ok(10)
    match a:
        case Ok(val):
            assert val == 10
        case _:
            assert False, "Wrong match branch"


def test_result_match_err():
    a: Result[float] = Err("Some weird error message")
    match a:
        case Err(e):
            assert e == "Some weird error message"
        case _:
            assert False, "Wrong match branch"


def test_result_type_match():
    a: Result[bool] = Err(ValueError("Some value error"))
    match a:
        case Err(ValueError() as e):
            assert e.args[0] == "Some value error"
        case Err(e):
            assert False, "Wrong error match branch"
        case _:
            assert False, "Wrong match branch"


def test_result_raise_error():
    a: Result[int] = Err(ValueError("Some error"))
    with pytest.raises(ValueError):
        match a:
            case Err(e):
                raise e
            case _:
                assert False, "Wrong match branch"


def test_ok_bools():
    a: Result[int] = Ok(10)
    assert a.is_ok()
    assert not a.is_err()


def test_err_bools():
    a: Result[int] = Err("Baasic error")
    assert not a.is_ok()
    assert a.is_err()


def test_ok_unwrap():
    a: Result[int] = Ok(10)
    res = a.unwrap()
    assert res == 10


def test_ok_unwrap_or():
    a: Result[int] = Ok(10)
    res = a.unwrap_or(20)
    assert res == 10


def test_err_unwrap():
    a: Result[int] = Err(ValueError("Some error"))
    with pytest.raises(ValueError):
        _ = a.unwrap()


def test_err_unwrap_or():
    a: Result[int] = Err("Some error")
    res = a.unwrap_or(20)
    assert res == 20


def test_ok_map():
    a: Result[int] = Ok(10)
    b = a.map(lambda x: 2 * x)
    assert isinstance(b, Ok) and b.value == 20


def test_ok_map_err():
    a: Result[int] = Ok(10)
    b = a.map_err(lambda x: 2 * x)
    assert isinstance(b, Ok) and b.value == 10


def test_err_map():
    a: Result[int] = Err("Error")
    b = a.map(lambda x: 2 * x)
    assert isinstance(b, Err) and b.error == "Error"


def test_err_map_err():
    a: Result[int] = Err("Error")
    b = a.map_err(lambda x: x.upper())
    assert isinstance(b, Err) and b.error == "ERROR"
