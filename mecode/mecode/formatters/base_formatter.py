# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from numbers import Number


class BaseFormatter(ABC):
    """Abstract base class for G-code formatting.

    Defines the interface that all G-code formatters must implement.
    """

    @abstractmethod
    def set_axis_label(self, axis: str, label: str) -> None:
        """Set a custom label for an axis.

        Args:
            axis: The axis to relabel
            label: The new label for the axis
        """

    @abstractmethod
    def set_comment_symbols(self, value: str) -> None:
        """Set the comment symbols for G-code comments.

        Args:
            value: Comment symbols to use
        """

    @abstractmethod
    def set_decimal_places(self, value: int) -> None:
        """Set the maximum decimal places for number formatting.

        Args:
            value: Number of decimal places
        """

    @abstractmethod
    def set_line_endings(self, line_endings: str) -> None:
        """Set the line ending style.

        Args:
            line_endings: Line ending style
        """

    @abstractmethod
    def format_number(self, number: Number) -> str:
        """Format a number with specified decimal places.

        Args:
            number: The number to format

        Returns:
            Formatted number string
        """

    @abstractmethod
    def format_line(self, statement: str) -> str:
        """Format a single G-code statement for output.

        Args:
            statement: The G-code statement to format

        Returns:
            Formatted statement with proper line endings
        """

    @abstractmethod
    def format_comment(self, text: str) -> str:
        """Format text as a G-code comment.

        Args:
            text: Text to be formatted as a comment

        Returns:
            Formatted comment string
        """

    @abstractmethod
    def format_command(self, command: str, params: dict = {}) -> str:
        """Format a G-code command with optional parameters.

        Args:
            command: The G-code command
            params: Command parameters

        Returns:
            Formatted command statement string
        """

    @abstractmethod
    def format_parameters(self, params) -> str:
        """Format G-code statement parameters.

        Args:
            params: Statement parameters

        Returns:
            Formatted parameters string
        """
