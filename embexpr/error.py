# coding: utf-8
import typing as ty


class ParseError(Exception):
    def __init__(self, message, location):  # type: (ty.Text, int) -> None
        super(ParseError, self).__init__(message)
        self.message = message  # type: ty.Text
        self.location = location  # type: int
