class FuckMeWhyNoDefaultIsProvidedWhenValueIsNotSetException(Exception):
    def __init__(self, field, *args: object) -> None:
        """Exception raised when fuck meee why no default is provided when value is not set"""
        self.field = field
        super().__init__(*args)

    def __str__(self) -> str:
        return (
            "Default value is not provided when value is not set for field '%s'"
            % self.field
        )


class UnsupportedDatabaseException(Exception):
    def __init__(self, db_type, *args: object) -> None:
        """Exception raised when model has unsupported db_type or none"""
        self.db_type = db_type
        super().__init__(*args)

    def __str__(self) -> str:
        return f"Unsupported database type {self.db_type}"


class MultiplePrimaryKeysException(Exception):
    def __init__(self, model, *args: object) -> None:
        """Exception raised when model has multiple primary keys"""
        super().__init__(*args)
        self.model = model

    def __str__(self) -> str:
        return (
            f"Model {self.model} has multiple primary keys; Which is not supported yet"
        )
