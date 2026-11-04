from dataclasses import dataclass


@dataclass
class Ok[T]:
    value: T


@dataclass
class Err[E]:
    error: E


type Result[T, E = str] = Ok[T] | Err[E]
