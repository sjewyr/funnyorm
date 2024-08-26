class ForeignKeyViolationException(Exception):
    """Raised when a foreign key violation is detected"""

    def __init__(self, table):
        super().__init__()
        self.table = table

    def __str__(self) -> str:
        return "Foreign key violation on table %s" % self.table
