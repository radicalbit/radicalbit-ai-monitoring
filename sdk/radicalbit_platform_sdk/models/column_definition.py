from pydantic import BaseModel


class ColumnDefinition(BaseModel):
    name: str
    type: str
