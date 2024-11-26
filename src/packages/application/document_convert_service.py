from typing import IO

from injector import inject, singleton

from packages.domain.document_extractor import DocumentExtractor

@singleton
class DocumentConvertService:
    @inject
    def __init__(self, extractor: DocumentExtractor) -> None:
        if not isinstance(extractor, DocumentExtractor):
            raise Exception("extractor is not DocumentExtractor.")

        self.extractor = extractor

    def extractDocument(self, document: IO) -> str:
        extract_doc = self.extractor.extract(document)
        return extract_doc.content
