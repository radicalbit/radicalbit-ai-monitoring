class BaseDAO:
    def attributes(self):
        return {c.key: getattr(self, c.key) for c in self.__mapper__.column_attrs}
