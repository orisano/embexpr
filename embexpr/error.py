# coding: utf-8
from typing import Text


class ParseError(Exception):
    def __init__(self, message, location):  # type: (Text, int) -> None
        super(ParseError, self).__init__(message)
        self.message = message  # type: Text
        self.location = location  # type: int
