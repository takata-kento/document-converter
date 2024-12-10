import pathlib
import shutil

from injector import inject, singleton

from packages.domain.document_extractor import DocumentExtractor
from packages.domain.pdf_generator import PdfGenerator

@singleton
class DocumentConvertService:
    @inject
    def __init__(self, extractor: DocumentExtractor, pdf_generator: PdfGenerator) -> None:
        if not isinstance(extractor, DocumentExtractor):
            raise Exception("extractor is not DocumentExtractor.")

        self.extractor = extractor
        self.pdf_generator = pdf_generator

    def extractDocument(self, source_dir: str, output_dir: str) -> None:
        tempdir = "./temp"

        for pdf in pathlib.Path(source_dir).glob('*.pdf'):
            with open(str(pdf), "rb") as file:
                paragraphs = self.extractor.extract(file)
                pathlib.Path(output_dir + '/' + pdf.name.split('.')[0] + ".md").write_bytes(paragraphs.content.replace("\n\n\n<table>", "\n\n<table>").encode())

        for docx in pathlib.Path(source_dir).glob('*.docx'):
            self.pdf_generator.generate(str(docx), tempdir)
            with open(tempdir + "/" + docx.name.split(".")[0] + ".pdf", "rb") as file:
                paragraphs = self.extractor.extract(file)
                pathlib.Path(output_dir + '/' + docx.name.split('.')[0] + ".md").write_bytes(paragraphs.content.replace("\n\n\n<table>", "\n\n<table>").encode())

        shutil.rmtree(tempdir)
