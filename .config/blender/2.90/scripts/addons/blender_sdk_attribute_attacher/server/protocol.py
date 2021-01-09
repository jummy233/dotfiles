"""
The implementation of the protocol between blender side server
and the unity side client. The protocol supports:
    - Transfer packed gltf data with attributes to unity.
    - Receive request for exported models, response with the list of objects
      currenlty in object_list.
    - Propagate error to client side.
"""

from dataclasses import dataclass
import abc
import json
from typing import Optional, Generic, TypeVar

T = TypeVar('T')
Json = str

# ------------------------------------------------------------------------
#    FromJson, ToJson abc
# ------------------------------------------------------------------------


class FromJson(abc.ABC, Generic[T]):
    def from_json(self, data: Json) -> Optional[T]:
        """
        Convert from json object to data type.
        """


class ToJson(abc.ABC):
    def to_json(self) -> Json:
        """
        Convert the data type into json.
        """


@dataclass(frozen=True)
class Request(FromJson):
    id: int
    message: str


@dataclass(frozen=True)
class Response(ToJson):
    id: int
    message: str


# ------------------------------------------------------------------------
#    Data type definition
# ------------------------------------------------------------------------


@dataclass(frozen=True)
class ObjectListRequest(FromJson):
    """
    Client request for model list.
    """
    id: int
    message: str

    def from_json(self, data: Json):
        NotImplemented


@dataclass(frozen=True)
class ObejctListResponse(ToJson):
    """
    Response to ObjectListRequest
    """
    id: int
    message: str

    def to_json(self):
        NotImplemented


@dataclass(frozen=True)
class ObjectModelRequest(FromJson):
    """
    Client requets for one specific model.
    """
    id: int
    model_id: int
    message: Optional[str]

    def from_json(self, data: Json):
        NotImplemented
