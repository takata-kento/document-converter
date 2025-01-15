from injector import Binder, Module, singleton

from packages.domain.document_extractor import DocumentExtractor
from packages.domain.document_intelligence_md_creator import DocumentIntelligenceMdCreator
from packages.domain.image_summarizer import ImageSummarizer
from packages.domain.md_creator import MdCreator
from packages.infrastructure.azure_document_extractor import AzureDocumentExtractor
from packages.infrastructure.azureoai_imgsummarizer import AzureOaiImgSummarizer

class DIContainer(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(DocumentExtractor, to=AzureDocumentExtractor, scope=singleton)
        binder.bind(ImageSummarizer, to=AzureOaiImgSummarizer, scope=singleton)
        binder.bind(MdCreator, to=DocumentIntelligenceMdCreator, scope=singleton)
