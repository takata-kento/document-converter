from typing import List
import subprocess

class PdfGenerator:
    def generate(self, document_path: str, outdir: str, timeout_sec: int = None) -> None:
        ret = subprocess.run(["soffice", "--headless", "--convert-to", "pdf", document_path, "--outdir", outdir],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=timeout_sec,
                check=True,
                text=True)
