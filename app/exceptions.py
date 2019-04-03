class NotFound(Exception):
    """Data not found"""


class InvalidException(Exception):
    """Custom base exception"""


class InvalidJson(InvalidException):
    """Cat't parse json from requests"""


class InvalidId(InvalidException):
    """Invalid id"""
