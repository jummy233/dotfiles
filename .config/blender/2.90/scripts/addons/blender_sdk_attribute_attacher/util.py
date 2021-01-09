
from dataclasses import dataclass
from typing import List


@dataclass
class Package:
    """
    The json format, contains both attributes and
    glb data.
    The glb data will be encoded in base64.
    """

    attribute_list: List[str]
    glb_base64_payload: str = ""

    def toJson(self):
        return self.__dict__


def Do(*args): return args[-1]


def Foreach(xs, f): return list(map(f, xs))


class _RecursiveCall(Exception):
    """
    mannual tail recursion optimization with exception.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


def recurse(*args, **kwargs):
    raise _RecursiveCall(*args, **kwargs)


def TRec(f):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except _RecursiveCall as e:
                args = e.args
                kwargs = e.kwargs
                continue
    return wrapper
