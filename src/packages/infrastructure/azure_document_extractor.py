"""Extracting documents by using Azure Document Intelligence.

This module provides class to extract various document.
"""
from os import environ
from typing import IO

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from injector import singleton

from packages.domain.document_extractor import DocumentExtractor

@singleton
class AzureDocumentExtractor(DocumentExtractor):
    """Extract document by using Azure Document Intelligence."""
    def __init__(self) -> None:
        self.key = environ.get('DI_KEY')
        self.endpoint = environ.get('DI_ENDPOINT')

    def extract(self, document: IO) -> AnalyzeResult:
        """Extract document by using Azure Document Intelligence.

        Args:
            document:
                Document to be extracted.

        Returns:
            JSON response of extracted document.
        """

        document_intelligence_client = DocumentIntelligenceClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key))
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout", analyze_request=document, content_type="application/octet-stream", output_content_format="markdown"
        )

        return poller.result().as_dict()
