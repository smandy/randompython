from dataclasses import dataclass

xs = range(1, 100)


class Foo:
    pass


@dataclass
class Baz:
    x: int


@dataclass
class Goo(Foo):
    x: int
    y: float


def add_to_string(a: int, b: int) -> str:
    return f"{a} + {b}"


def mergeDict(x: dict[int, str],
              y: dict[int, str]) -> dict[int, str]:
    ret: dict[int, str] = {}
    ret.update(x)
    ret.update(y)
    return ret


a2 = {32: "foo"}
b2 = {51: "bar"}

mergeDict(a2, b2)


def mergeDict2(x: dict[int, Goo],
               y: dict[int, Goo]) -> dict[int, Goo]:
    ret: dict[int, Goo] = {}
    ret.update(x)
    ret.update(y)
    return ret


mergeDict2({1: Goo(10, 2.3)}, {2: Goo(20, 6.7)})
mergeDict2({1: Goo(10, 4.5)}, {2: Goo(20, 21.3)})


def acceptFoo(x: Foo):
    print(f"Woohoo I got a foo {x}")


acceptFoo(Foo())
acceptFoo(Goo(21, 69.0))


def names(x2: set[str]) -> set[str]:
    return x2


arg: set[str] = {"foo", "bar", "21"}
print(names(arg))


def doit(s: set[str]):
    print(f"s is {s}")


doit({"foo", "21"})
