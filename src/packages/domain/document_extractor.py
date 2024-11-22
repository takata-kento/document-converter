from abc import ABCMeta, abstractmethod
from typing import List, Optional, IO

from azure.ai.documentintelligence.models import AnalyzeResult

class DocumentExtractor(metaclass=ABCMeta):
    @abstractmethod
    def extract(self, document: IO) -> AnalyzeResult:
        raise NotImplementedError()
