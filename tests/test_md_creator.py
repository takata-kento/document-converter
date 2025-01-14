import json
import os
import sys
import unittest

from unittest.mock import MagicMock
from azure.ai.documentintelligence.models import AnalyzeResult

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../src'
        )
    )
)
import src.packages.domain.md_creator as md_creator
import src.packages.domain.image_extractor as image_extractor
import src.packages.domain.image_summarizer as image_summarizer

class TestMdCreator(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.img_extractor = MagicMock(spec=image_extractor.ImageExtractor)
        self.img_summarizer = MagicMock(spec=image_summarizer.ImageSummarizer)
        self.md_creator = md_creator.MdCreator(self.img_extractor, self.img_summarizer)

    def test_create(self):
        # Given
        with open("tests/fixtures/sample_document_intelligence_result.json") as json_test_data:
            json_load = json.load(json_test_data)
            analyze_result = AnalyzeResult(json_load)

        self.img_extractor.extract.return_value = "extracted_image_data"
        self.img_summarizer.summarize.return_value = "summarized_text"

        pdf_path = "dummy_path.pdf"
        expect_md_str = '''# This is title


## 1. Text

Latin refers to an ancient Italic language originating in the region of Latium in ancient Rome.


## 2. Page Objects


## 2.1 Table

Here's a sample table below, designed to be simple for easy understand and quick reference.
<table>
<tr>
<th>Name</th>
<th>Corp</th>
<th>Remark</th>
</tr>
<tr>
<td>Foo</td>
<td></td>
<td></td>
</tr>
<tr>
<td>Bar</td>
<td>Microsoft</td>
<td>Dummy</td>
</tr>
</table>

Table 1: This is a dummy table


## 2.2. Figure

Figure 1: Here is a figure with text
[この部分にはもともと画像情報が添付されていました。画像情報の要約は以下になります。]
(summarized_text)


## 3. Others

AI Document Intelligence is an AI service that applies advanced machine learning to extract text, key-value pairs, tables, and structures from documents automatically and accurately:

:selected: clear

:selected: precise

:unselected: vague

:selected: coherent

:unselected: Incomprehensible

Turn documents into usable data and shift your focus to acting on information rather than compiling it. Start with prebuilt models or create custom models tailored to your documents both on premises and in the cloud with the AI Document Intelligence studio or SDK.

Learn how to accelerate your business processes by automating text extraction with AI Document Intelligence. This webinar features hands-on demos for key use cases such as document processing, knowledge mining, and industry-specific AI model customization.
'''

        # When
        context = self.md_creator.create(analyze_result, pdf_path)

        # Then
        self.assertEqual(expect_md_str, context)

if __name__ == '__main__':
    unittest.main()
