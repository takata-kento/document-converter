"""Extracting image from PDF.

This module provides class to extract image from PDF file.

Typical usage example:

  page_number = 1
  bounding_box = [0, 0, 100, 100]
  image_extractor = ImageExtractor()
  output_file_path = image_extractor.extract("path/to/pdffile",
                                             page_number,
                                             "path/to/outputdir",
                                             bounding_box)
"""

from typing import List
import pathlib
import time

import fitz

class ImageExtractor:
    """Extract image from PDF."""
    def extract(self, pdf_path: str,
                page_number: int,
                outdir: str,
                bounding_box: List[float]
                ) -> str | None:
        """Extract image from PDF.

        Retrieves image and saves it to outdir as 'png' file.

        Args:
            pdf_path:
                Path to PDF file.
            page_number:
                Page number to extract image from.
            outdir:
                Directory to save image.
            bounding_box:
                Bounding box coordinates of the image to extract.
                Requires the coordinates in the format (x0, y0, x1, y1).
                x0, y0 represents the top-left corner and x1, y1 represents the bottom-right corner.
                The coordinates are in points. 1point equals 1/72 inch.

        Returns:
            output file name if successful, None otherwise.
            example: 

            'foo/bar/foobar_123456789.png'
            if you have a pdf file named 'foobar.pdf' and you set the outdir to 'foo/bar/'.
        """

        pdx = page_number - 1
        pdf_name = pathlib.Path(pdf_path).name.split('.')[0]
        output_file_path = outdir + '/' + pdf_name + "_" + str(time.time_ns()) + ".png"

        if not pathlib.Path(outdir).exists():
            pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)

        try:
            with fitz.open(pdf_path) as doc:
                page = doc.load_page(pdx)

                rect = fitz.Rect(bounding_box)
                pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72), clip=rect)

                pathlib.Path(output_file_path).write_bytes(pix.tobytes())

                return output_file_path
        except (fitz.FileDataError, fitz.FileNotFoundError) as e:
            print(f"Error: {e}")
            return None
