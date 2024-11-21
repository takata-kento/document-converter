from injector import Binder, Module, singleton

from packages.domain.document_extractor import DocumentExtractor
from packages.infrastructure.azure_document_extractor import AzureDocumentExtractor
from packages.application.document_convert_service import DocumentConvertService

class DIContainer(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(DocumentExtractor, to=AzureDocumentExtractor, scope=singleton)
        binder.bind(DocumentConvertService, to=DocumentConvertService, scope=singleton)
