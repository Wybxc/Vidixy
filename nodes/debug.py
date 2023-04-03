import vidixy


@vidixy.node()
@vidixy.control("Number", default=1)
@vidixy.output("number", socket="Number")
def number(i: int) -> int:
    return i


@vidixy.node()
@vidixy.input("a", socket="Number")
@vidixy.input("b", socket="Number")
@vidixy.output("sum", socket="Number")
def add(a: int, b: int) -> int:
    return a + b
