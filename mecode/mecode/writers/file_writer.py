# -*- coding: utf-8 -*-

from typing import Union, TextIO, BinaryIO

from .base_writer import BaseWriter


class FileWriter(BaseWriter):
    """Writer that outputs commands to a file or file-like object.

    This class implements a G-code writer that can write G-code commands
    to a file. The writer handles both text and binary output modes
    automatically, converting between bytes and strings as needed.

    Example:
        >>> writer = FileWriter("output.gcode")
        >>> writer.write(b"G1 X10 Y10\\n")
        >>> writer.disconnect()
    """

    def __init__(self, output: Union[str, TextIO, BinaryIO]):
        """Initialize the file writer.

        Args:
            output (Union[str, TextIO, BinaryIO]): Either a file path
                or a file-like object to write the G-code to.
        """

        self._output = output
        self._file = None

    def connect(self) -> None:
        """Establish the connection to the output file."""

        self._file = self._output

        if isinstance(self._output, str):
            self._file = open(self._output, "wb+")

    def disconnect(self, wait: bool = True) -> None:
        """Close the file if it was opened by this writer."""

        should_close = isinstance(self._output, str)

        if should_close and self._file is not None:
            self._file.close()
            self._file = None

    def write(self, statement: bytes, requires_response: bool = False) -> None:
        """Write a G-code statement to the file.

        Args:
            statement (bytes): The G-code statement to write.
        """

        if self._file is None:
            self.connect()

        if hasattr(self._file, 'encoding'):
            statement = statement.decode("utf-8")

        self._file.write(statement)

        if hasattr(self._file, 'flush'):
            self._file.flush()

        return None
