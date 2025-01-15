"""Extracting documents.

This module provides class to extract various document.
"""
from abc import ABCMeta, abstractmethod
from typing import IO

class DocumentExtractor(metaclass=ABCMeta):
    """Extract document"""

    @abstractmethod
    def extract(
        self,
        document: IO
    ) -> dict[str, any]:
        """Extract document by using Cloud Service.

        Args:
            document:
                Document to be extracted.

        Returns:
            JSON response of extracted document.
        """

        raise NotImplementedError()
