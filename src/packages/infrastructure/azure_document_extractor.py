from os import environ
from typing import List, Optional, IO

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from injector import singleton

from packages.domain.document_extractor import DocumentExtractor

@singleton
class AzureDocumentExtractor(DocumentExtractor):
    def __init__(self) -> None:
        self.key = environ.get('DI_KEY')
        self.endpoint = environ.get('DI_ENDPOINT')

    def extract(self, document: IO) -> Optional[List[str]]:
        document_intelligence_client = DocumentIntelligenceClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key))
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", analyze_request=document, content_type="application/octet-stream"
        )

        result: AnalyzeResult = poller.result()
        if result.paragraphs:
            result.paragraphs.sort(key=lambda p: (p.spans.sort(key=lambda s: s.offset), p.spans[0].offset))

            return [paragraph.content for paragraph in result.paragraphs]
