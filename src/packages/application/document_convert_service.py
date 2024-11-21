from typing import List, Optional, IO

from injector import inject, singleton

from packages.domain.document_extractor import DocumentExtractor

@singleton
class DocumentConvertService:
    @inject
    def __init__(self, extractor: DocumentExtractor) -> None:
        if not isinstance(extractor, DocumentExtractor):
            raise Exception("extractor is not DocumentExtractor.")

        self.extractor = extractor

    def extractDocument(self, document: IO) -> Optional[List[str]]:
        return self.extractor.extract(document)
