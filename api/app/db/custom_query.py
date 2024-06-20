from abc import ABC

from sqlalchemy.orm import Query


class CustomQuery(Query, ABC):
    def filter_if(self: Query, condition: bool, *criterion):
        if condition:
            return self.filter(*criterion)
        return self
