import pathlib
import shutil

from injector import inject, singleton

from packages.domain.document_extractor import DocumentExtractor
from packages.domain.pdf_generator import PdfGenerator
from packages.domain.image_extractor import ImageExtractor

@singleton
class DocumentConvertService:
    @inject
    def __init__(self, extractor: DocumentExtractor, pdf_generator: PdfGenerator, img_extractor: ImageExtractor) -> None:
        if not isinstance(extractor, DocumentExtractor):
            raise Exception("extractor is not DocumentExtractor.")

        self.extractor = extractor
        self.pdf_generator = pdf_generator
        self.img_extractor = img_extractor

    def extractDocument(self, source_dir: str, output_dir: str) -> None:
        tempdir = "./temp"

        for pdf in pathlib.Path(source_dir).glob('*.pdf'):
            with open(str(pdf), "rb") as file:
                paragraphs = self.extractor.extract(file)
                pathlib.Path(output_dir + '/' + pdf.name.split('.')[0] + ".md").write_bytes(paragraphs.content.replace("\n\n\n<table>", "\n\n<table>").encode())

                if paragraphs.figures:
                    for figure in paragraphs.figures:
                        page_number = figure.bounding_regions[0].page_number
                        cordinates = [figure.bounding_regions[0].polygon[0] * 72, figure.bounding_regions[0].polygon[1] * 72, figure.bounding_regions[0].polygon[4] * 72, figure.bounding_regions[0].polygon[5] * 72]
                        self.img_extractor.extract(str(pdf), page_number, tempdir, cordinates)


        for docx in pathlib.Path(source_dir).glob('*.docx'):
            temp_pdffile_path = tempdir + "/" + docx.name.split(".")[0] + ".pdf"
            output_mdfile_path = output_dir + '/' + docx.name.split('.')[0] + ".md"

            self.pdf_generator.generate(str(docx), tempdir)

            with open(temp_pdffile_path, "rb") as file:
                paragraphs = self.extractor.extract(file)
                pathlib.Path(output_mdfile_path).write_bytes(paragraphs.content.replace("\n\n\n<table>", "\n\n<table>").encode())
                
                if paragraphs.figures:
                    for figure in paragraphs.figures:
                        page_number = figure.bounding_regions[0].page_number
                        cordinates = [figure.bounding_regions[0].polygon[0] * 72, figure.bounding_regions[0].polygon[1] * 72, figure.bounding_regions[0].polygon[4] * 72, figure.bounding_regions[0].polygon[5] * 72]
                        self.img_extractor.extract(temp_pdffile_path, page_number, tempdir, cordinates)

        shutil.rmtree(tempdir)
