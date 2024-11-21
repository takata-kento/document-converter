import sys
from os import environ

from injector import inject, Injector
from dotenv import load_dotenv

from packages.presentation.document_convert_controller import DocumentConvertController
from packages.dicontainer.di_container import DIContainer

if __name__ == "__main__":
    load_dotenv()
    key = environ.get('DI_KEY')
    endpoint = environ.get('DI_ENDPOINT')
    source_dir = "./source"
    output_dir = "./output"

    injector = Injector([DIContainer()])
    controller: DocumentConvertController = injector.get(DocumentConvertController)

    controller.batch_convert_local_files(source_dir, output_dir)
