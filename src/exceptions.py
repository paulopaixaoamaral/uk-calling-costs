class RepositoryException(Exception):
    pass


class InvalidCostType(RepositoryException):
    pass


class UnknownCountry(RepositoryException):
    pass


class MissingCountryData(RepositoryException):
    pass
