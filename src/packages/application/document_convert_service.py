import pathlib
import shutil

from injector import inject, singleton

from packages.domain.document_extractor import DocumentExtractor
from packages.domain.pdf_generator import PdfGenerator
from packages.domain.image_extractor import ImageExtractor
from packages.domain.image_summarizer import ImageSummarizer
from packages.domain.md_creator import MdCreator

@singleton
class DocumentConvertService:
    @inject
    def __init__(
        self,
        extractor: DocumentExtractor,
        pdf_generator: PdfGenerator,
        img_extractor: ImageExtractor,
        img_summarizer: ImageSummarizer,
        md_creator: MdCreator
    ) -> None:
        self.extractor = extractor
        self.pdf_generator = pdf_generator
        self.img_extractor = img_extractor
        self.img_summarizer = img_summarizer
        self.md_creator = md_creator

    def extractDocument(self, source_dir: str, output_dir: str) -> None:
        tempdir = "./temp"

        if not pathlib.Path(tempdir).exists():
            pathlib.Path(tempdir).mkdir(parents=True, exist_ok=True)

        for docx in pathlib.Path(source_dir).glob('*.docx'):
            temp_pdffile_path = tempdir + "/" + docx.name.split(".")[0] + ".pdf"
            self.pdf_generator.generate(str(docx), tempdir)

        for pdf in pathlib.Path(source_dir).glob('*.pdf'):
            shutil.copy(str(pdf), tempdir)

        for source in pathlib.Path(tempdir).glob('*.pdf'):
            with open(str(source), "rb") as file:
                paragraphs = self.extractor.extract(file)
                pathlib.Path(
                        output_dir + '/' + source.name.split('.')[0] + ".md"
                    ).write_bytes(
                        self.md_creator.create(paragraphs, str(source)).encode()
                    )

        shutil.rmtree(tempdir)
