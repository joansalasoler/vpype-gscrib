# -*- coding: utf-8 -*-

from .base_writer import BaseWriter
from ..utils.printer import Printer


class SerialWriter(BaseWriter):
    """Writer that sends commands through a serial connection.

    This class implements a G-code writer that connects to a device
    through a serial port and sends G-code commands to it. It uses a
    `Printer` object to manage the serial communication.

    Example:
        >>> writer = SerialWriter("/dev/ttyUSB0", 115200)
        >>> writer.write(b"G1 X10 Y10\n")
        >>> writer.disconnect()"
    """

    def __init__(self, port: str, baudrate: int):
        """Initialize the serial writer.

        Args:
            port (str): Serial port identifier
            baudrate (int): Communication speed in bauds
        """

        self._printer = None
        self._baudrate = baudrate
        self._port = port

    def connect(self) -> None:
        """Establish the serial connection to the device.

        Creates a `Printer` object with the configured port and baudrate,
        connects to the device, and starts the communication.

        Raises:
            SerialException: If the connection cannot be established.
        """

        self._printer = Printer(self._port, self._baudrate)
        self._printer.connect()
        self._printer.start()

    def disconnect(self, wait: bool = True) -> None:
        """Close the serial connection if it exists.

        Args:
            wait (bool): If True, waits for any pending operations to
                complete before disconnecting.
        """

        if self._printer is not None:
            self._printer.disconnect(wait)
            self._printer = None

    def write(self,
        statement: bytes, requires_response: bool = False) -> str | None:
        """Send a G-code statement through the serial connection.

        Automatically establishes the connection if not already connected.
        Can optionally wait for and return a response from the device.

        Args:
            statement (bytes): The G-code statement to send.
            requires_response (bool, optional): Whether to wait for a
                response from the device.

        Returns:
            Optional[str]: Response from the device.

        Raises:
            SerialException: If there are communication errors.
        """

        statement_str = statement.decode("utf-8")

        if self._printer is None:
            self.connect()

        if requires_response:
            return self._printer.get_response(statement_str)

        self._printer.sendline(statement_str)
        return None
