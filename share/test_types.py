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
