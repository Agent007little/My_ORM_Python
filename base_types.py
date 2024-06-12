class BaseType:
    field_type: str  # название типа данных поля, например, "INTEGER"

    def __init__(self, unique: bool = False, null: bool = True, default: int = None):
        self.unique = unique
        self.null = null
        self.default = default


class IntegerField(BaseType):
    field_type = 'INTEGER'


class VarcharField(BaseType):
    field_type = 'VARCHAR'
