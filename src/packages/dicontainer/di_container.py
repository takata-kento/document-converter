from injector import Binder, Module, singleton

from packages.domain.document_extractor import DocumentExtractor
from packages.infrastructure.azure_document_extractor import AzureDocumentExtractor
from packages.domain.image_summarizer import ImageSummarizer
from packages.infrastructure.azureoai_imgsummarizer import AzureOaiImgSummarizer

class DIContainer(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(DocumentExtractor, to=AzureDocumentExtractor, scope=singleton)
        binder.bind(ImageSummarizer, to=AzureOaiImgSummarizer, scope=singleton)
