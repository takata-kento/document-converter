import pathlib

from injector import inject

from packages.application.document_convert_service import DocumentConvertService

class DocumentConvertController:
    @inject
    def __init__(self, convert_service: DocumentConvertService) -> None:
        if not isinstance(convert_service, DocumentConvertService):
            raise Exception("convert_service is not DocumentConvertService.")

        self.convert_service = convert_service

    def batch_convert_local_files(self, source_dir: str, output_dir: str) -> int:
        if not pathlib.Path(source_dir).exists:
            raise RuntimeError(f"{source_dir} is not exists.")

        if not pathlib.Path(output_dir).exists:
            pathlib.Path(output_dir).mkdir()

        if not [file for file in pathlib.Path(source_dir).iterdir() if file.is_file()]:
            raise RuntimeError(f"{source_dir} has no files.")

        for pdf in pathlib.Path(source_dir).glob('*.pdf'):
            with open(str(pdf), "rb") as file:
                paragraphs = self.convert_service.extractDocument(file)
                pathlib.Path(output_dir + '/' + pdf.name.split('.')[0] + ".md").write_bytes('\n\n'.join(paragraphs).encode())

        for pdf in pathlib.Path(source_dir).glob('*.docx'):
            with open(str(pdf), "rb") as file:
                paragraphs = self.convert_service.extractDocument(file)
                pathlib.Path(output_dir + '/' + pdf.name.split('.')[0] + ".md").write_bytes('\n\n'.join(paragraphs).encode())
