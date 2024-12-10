import pathlib

from injector import inject, singleton

from packages.domain.document_extractor import DocumentExtractor

@singleton
class DocumentConvertService:
    @inject
    def __init__(self, extractor: DocumentExtractor) -> None:
        if not isinstance(extractor, DocumentExtractor):
            raise Exception("extractor is not DocumentExtractor.")

        self.extractor = extractor

    def extractDocument(self, source_dir: str, output_dir: str) -> None:
        for pdf in pathlib.Path(source_dir).glob('*.pdf'):
            with open(str(pdf), "rb") as file:
                paragraphs = self.extractor.extract(file)
                pathlib.Path(output_dir + '/' + pdf.name.split('.')[0] + ".md").write_bytes(paragraphs.content.replace("\n\n\n<table>", "\n\n<table>").encode())

        for docx in pathlib.Path(source_dir).glob('*.docx'):
            with open(str(docx), "rb") as file:
                paragraphs = self.extractor.extract(file)
                pathlib.Path(output_dir + '/' + docx.name.split('.')[0] + ".md").write_bytes(paragraphs.content.replace("\n\n\n<table>", "\n\n<table>").encode())
