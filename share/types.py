from dataclasses import dataclass
from typing import Callable, Never


@dataclass(frozen=True)
class Ok[T]:
    value: T

    def is_ok(self: "Ok") -> bool: return True

    def is_err(self: "Ok") -> bool: return False

    def unwrap(self: "Ok") -> T:
        return self.value

    def unwrap_or(self: "Ok", default: T) -> T:
        return self.value

    def map[U](self: "Ok", func: Callable[[T], U]) -> "Ok[T]":
        return Ok(func(self.value))

    def map_err[E, U](self: "Ok", func: Callable[[E], U]) -> "Ok[T]":
        return self


@dataclass(frozen=True)
class Err[E]:
    error: E

    def is_ok(self: "Err") -> bool: return False

    def is_err(self: "Err") -> bool: return True

    def unwrap(self: "Err") -> Never:
        # panic
        raise self.error

    def unwrap_or[T](self: "Err", default: T) -> T:
        return default

    def map[T, U](self: "Err", func: Callable[[T], U]) -> "Err[E]":
        return self

    def map_err[U](self: "Err", func: Callable[[E], U]) -> "Err[U]":
        return Err(func(self.error))


type Result[T, E = str] = Ok[T] | Err[E]
