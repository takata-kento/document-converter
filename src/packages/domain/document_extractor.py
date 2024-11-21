from abc import ABCMeta, abstractmethod
from typing import List, Optional, IO

class DocumentExtractor(metaclass=ABCMeta):
    @abstractmethod
    def extract(self, document: IO) -> Optional[List[str]]:
        raise NotImplementedError()
