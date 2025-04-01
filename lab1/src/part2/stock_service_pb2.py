# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stock_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13stock_service.proto\"\"\n\x0cStockCompany\x12\x12\n\nstock_name\x18\x01 \x01(\t\"J\n\tStockInfo\x12\r\n\x05price\x18\x01 \x01(\x02\x12\x1b\n\x0etrading_volume\x18\x02 \x01(\x05H\x00\x88\x01\x01\x42\x11\n\x0f_trading_volume\"U\n\x0bTradingInfo\x12\x12\n\nstock_name\x18\x01 \x01(\t\x12\x16\n\x0etrading_volume\x18\x02 \x01(\x05\x12\x1a\n\x04type\x18\x03 \x01(\x0e\x32\x0c.TradingType\"#\n\x0fTradingResponse\x12\x10\n\x08response\x18\x01 \x01(\x05\"0\n\x0bStockUpdate\x12\x12\n\nstock_name\x18\x01 \x01(\t\x12\r\n\x05price\x18\x02 \x01(\x02\"\"\n\x0eUpdateResponse\x12\x10\n\x08response\x18\x01 \x01(\x05* \n\x0bTradingType\x12\x07\n\x03\x42UY\x10\x00\x12\x08\n\x04SELL\x10\x01\x32\x8b\x01\n\x0cStockService\x12%\n\x06Lookup\x12\r.StockCompany\x1a\n.StockInfo\"\x00\x12)\n\x05Trade\x12\x0c.TradingInfo\x1a\x10.TradingResponse\"\x00\x12)\n\x06Update\x12\x0c.StockUpdate\x1a\x0f.UpdateResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stock_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TRADINGTYPE._serialized_start=345
  _TRADINGTYPE._serialized_end=377
  _STOCKCOMPANY._serialized_start=23
  _STOCKCOMPANY._serialized_end=57
  _STOCKINFO._serialized_start=59
  _STOCKINFO._serialized_end=133
  _TRADINGINFO._serialized_start=135
  _TRADINGINFO._serialized_end=220
  _TRADINGRESPONSE._serialized_start=222
  _TRADINGRESPONSE._serialized_end=257
  _STOCKUPDATE._serialized_start=259
  _STOCKUPDATE._serialized_end=307
  _UPDATERESPONSE._serialized_start=309
  _UPDATERESPONSE._serialized_end=343
  _STOCKSERVICE._serialized_start=380
  _STOCKSERVICE._serialized_end=519
# @@protoc_insertion_point(module_scope)
