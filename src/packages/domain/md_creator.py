"""Creating MarkDown context.

This module provides class to create markdown context from various API result.
"""
from abc import ABCMeta, abstractmethod

class MdCreator(metaclass=ABCMeta):
    """Create MarkDown context"""

    @abstractmethod
    def create(
        self,
        analyze_result: dict[str, any],
        source_pdf_path: str
    ) -> str:
        """Create MarkDown context from various API result.

        Args:
            analyze_result:
                result of extracting file.
                this represents API JSON response.
            source_pdf_path:
                Extracted Source file by Azure Document Intelligence.
                This path is consistent with the file used in the analyze_result.

        Returns:
            MarkDown context.
            example: 

            '# 1 Title\n\n\n## 1.1 SubTitle\n\nHello\n\nWorld.'
        """

        raise NotImplementedError()
