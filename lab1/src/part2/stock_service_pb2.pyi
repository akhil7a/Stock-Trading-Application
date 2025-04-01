from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

BUY: TradingType
DESCRIPTOR: _descriptor.FileDescriptor
SELL: TradingType

class StockCompany(_message.Message):
    __slots__ = ["stock_name"]
    STOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    stock_name: str
    def __init__(self, stock_name: _Optional[str] = ...) -> None: ...

class StockInfo(_message.Message):
    __slots__ = ["price", "trading_volume"]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    TRADING_VOLUME_FIELD_NUMBER: _ClassVar[int]
    price: float
    trading_volume: int
    def __init__(self, price: _Optional[float] = ..., trading_volume: _Optional[int] = ...) -> None: ...

class StockUpdate(_message.Message):
    __slots__ = ["price", "stock_name"]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    STOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    price: float
    stock_name: str
    def __init__(self, stock_name: _Optional[str] = ..., price: _Optional[float] = ...) -> None: ...

class TradingInfo(_message.Message):
    __slots__ = ["stock_name", "trading_volume", "type"]
    STOCK_NAME_FIELD_NUMBER: _ClassVar[int]
    TRADING_VOLUME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    stock_name: str
    trading_volume: int
    type: TradingType
    def __init__(self, stock_name: _Optional[str] = ..., trading_volume: _Optional[int] = ..., type: _Optional[_Union[TradingType, str]] = ...) -> None: ...

class TradingResponse(_message.Message):
    __slots__ = ["response"]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: int
    def __init__(self, response: _Optional[int] = ...) -> None: ...

class UpdateResponse(_message.Message):
    __slots__ = ["response"]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: int
    def __init__(self, response: _Optional[int] = ...) -> None: ...

class TradingType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
