from enum import Enum


class OrderType(str, Enum):
    ASC = 'asc'
    DESC = 'desc'
