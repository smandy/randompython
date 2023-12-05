#!/usr/bin/env python

# C-c ! l to list pycheckers errors

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Person:
    name: str
    age: int
    fwends: list[str] = field(default_factory=list)


a = Person(name='andy', age=30, fwends=['chris', 'jamie'])
b = Person(name='audrey', age=52)


def doit(x: int) -> None:
    print(f"Doit {x}")


doit(21)


def doSplit(x: str) -> None:
    match x.split(','):
        case [a2, b2]:
            print(f"Woot {a2} {b2}")
        case [a2]:
            print(f"Toot {a2}")
        case _:
            print("Does not compute")


doSplit("foo,bar")
doSplit("foo")
doSplit("foo,bar,baz")
