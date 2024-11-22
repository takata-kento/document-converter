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
        result = self.extractor.extract(document)
        if result.paragraphs:
            result.paragraphs.sort(key=lambda p: (p.spans.sort(key=lambda s: s.offset), p.spans[0].offset))

            return [paragraph.content for paragraph in result.paragraphs]
