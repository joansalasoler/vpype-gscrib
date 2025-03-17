# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class BaseWriter(ABC):
    """Base class for all the G-code writing implementations.

    This class defines the interface for writing G-code commands to various
    outputs, such as files, serial connections, or network sockets.
    """

    @abstractmethod
    def connect(self) -> None:
        """Establish connection or open resource for writing"""

    @abstractmethod
    def disconnect(self, wait: bool = True) -> None:
        """Close connection or resource"""

    @abstractmethod
    def write(self,
        statement: bytes, requires_response: bool = False) -> str | None:
        """Write G-code statement and optionally get response"""
