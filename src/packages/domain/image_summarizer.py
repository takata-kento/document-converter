"""Summarize image.

This module provides class to summarize image.

Typical usage example:
    class SomeClass:
        def __init__(
                self,
                image_summarizer: ImageSummarizer
        ) -> None:
            self.image_summarizer = image_summarizer

        def some_method(
                self
        ):
            summary = self.image_summarizer.summarize("path/to/image.png")

"""

from abc import ABCMeta, abstractmethod

class ImageSummarizer(metaclass=ABCMeta):
    """Summarize image."""
    @abstractmethod
    def summarize(
           self,
           img_path: str
    ) -> str:
        """Summarize image.

        Summarize png image file.

        Args:
            img_path:
                Path to image file.

        Returns:
            Summary of the image as str.
        """

        raise NotImplementedError()
