"""Creating MarkDown context from Azure Document Intelligence result.

This module provides class to create markdown context from Azure Document Intelligence result.

Typical usage example:
    class SomeClass:
        def __init__(
                self,
                md_creator: DocumentIntelligenceMdCreator
        ) -> None:
            self.md_creator = md_creator

        def some_method(
                self,
                document: IO,
                source_pdf_path: str
        ):
            document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
            result = document_intelligence_client.begin_analyze_document(
                "prebuilt-layout", analyze_request=document, content_type="application/octet-stream", output_content_format="markdown"
            ).result()

            context = self.md_creator.create(result.as_dict(), source_pdf_path)
"""
from azure.ai.documentintelligence.models import AnalyzeResult, DocumentTableCell, DocumentTableCellKind
from injector import inject, singleton

from packages.domain.image_extractor import ImageExtractor
from packages.domain.image_summarizer import ImageSummarizer
from packages.domain.md_creator import MdCreator

@singleton
class DocumentIntelligenceMdCreator(MdCreator):
    """Create MarkDown context from Azure Document Intelligence result."""

    @inject
    def __init__(
            self,
            img_extractor: ImageExtractor,
            img_summarizer: ImageSummarizer
    ) -> None:

        self.img_extractor = img_extractor
        self.img_summarizer = img_summarizer

    def create(
            self,
            analyze_result: dict[str, any],
            source_pdf_path: str
    ) -> str:
        """Create MarkDown context from Azure Document Intelligence result.

        Args:
            analyze_result:
                Azure Document Intelligence result of extracting file.
            source_pdf_path:
                Extracted Source file by Azure Document Intelligence.
                This path is consistent with the file used in the analyze_result.

        Returns:
            MarkDown context.
            example: 

            '# 1 Title\n\n\n## 1.1 SubTitle\n\nHello\n\nWorld.'
        """

        all_markdown = ''

        document_intelligence_result = AnalyzeResult(analyze_result)

        paragraphs = self.__get_paragraphs(document_intelligence_result)
        tables = self.__get_markdown_tables(document_intelligence_result)

        section_elements = self.__get_section_elements(document_intelligence_result)
        for element in section_elements:
            if element.startswith('/paragraphs/'):
                is_first_line = all_markdown == ''
                all_markdown += self.__get_markdown_paragraph(
                    paragraphs[element]['role'],
                    paragraphs[element]['content'],
                    is_first_line
                )
            elif element.startswith('/figures/'):
                idx = int(element.split('/')[-1])
                all_markdown += self.__get_figure_summarize(idx, document_intelligence_result, source_pdf_path)
            elif element.startswith('/tables/'):
                idx = int(element.split('/')[-1])
                all_markdown += tables[element]
            else:
                continue

            all_markdown += '\n'
        return all_markdown

    def __get_paragraphs(
            self,
            analyze_result: AnalyzeResult
    ) -> dict[str, dict[str, str]]:
        """Get paragraphs from Azure Document Intelligence response.
        paragraphs is one of the JSON attributes in the response.

        Args:
            analyze_result:
                Azure Document Intelligence result of extracting file.

        Returns:
            paragraphs dictionary.
            this dictionary has paragraph id as key. ex) "/paragraphs/0"
            and a paragraph is also dictionary whitch has id, content, role, polygon and pageNumber as key.
        """

        paragraphs = {}
        for idx, paragraph in enumerate(analyze_result.paragraphs):
            item = {
                "id": "/paragraphs/" + str(idx),
                "content": paragraph.content if paragraph.content else "",
                "role": paragraph.role if paragraph.role else "",
                "polygon": paragraph.get("boundingRegions")[0]["polygon"],
                "pageNumber": paragraph.get("boundingRegions")[0]["pageNumber"]
            }
            paragraphs["/paragraphs/" + str(idx)] = item
        return paragraphs

    def __get_section_elements(
            self,
            analyze_result: AnalyzeResult
    ) -> list[str]:
        """Get elements from Azure Document Intelligence response.
        elements is part of sections whitch is one of the JSON attributes in the response.
        element represents a paragraph, table, figure, or other in the extracted document.

        Args:
            analyze_result:
                Azure Document Intelligence result of extracting file.

        Returns:
            elements
        """

        section_elements = []
        for section in analyze_result.sections:
            section_elements.extend(section.elements) 
        return section_elements

    def __get_markdown_tables(
            self,
            analyze_result: AnalyzeResult
    ) -> dict[str, str]:
        """Get markdown tables from Azure Document Intelligence response.

        Args:
            analyze_result:
                Azure Document Intelligence result of extracting file.

        Returns:
            dictionary of markdown tables.
            example: 

            {
                "/tables/0" : "<table>\n<tr>\n<th>HEADER1</th>\n<th>HEADER2</th>\n</tr>\n<tr>\n<td>DATA1</td>\n<td>DATA2</td>\n</tr>\n</table>",
                "/tables/1" : "<table>\n<tr>\n<th>FOO</th>\n<th>BAR</th>\n</tr>\n<tr>\n<td>foo</td>\n<td>bar</td>\n</tr>\n</table>"
            }
        """

        tables = {}

        for idx, table in enumerate(analyze_result.tables):
            table_data = "<table>\n<tr>\n"

            for cell_idx, cell in enumerate(table.cells):
                if self.__check_new_row(cell_idx, table.cells):
                    table_data += "</tr>\n<tr>\n"
                
                if (cell.kind == DocumentTableCellKind.COLUMN_HEADER) | (cell.kind == DocumentTableCellKind.ROW_HEADER):
                    table_data += self.__create_table_header(cell)
                else:
                    table_data += self.__create_table_data(cell)

            table_data += "</tr>\n</table>"
            tables["/tables/" + str(idx)] = table_data

        return tables

    def __check_new_row(
            self,
            cell_idx: int,
            cell_list: list[DocumentTableCell]
    ) -> bool:
        """Check wheather the new row or not.

        Args:
            cell_idx:
                Index of cell in the cell list.
            cell_list:
                List of cells in the table.

        Returns:
            True if the new row starts, False otherwise.
        """

        if cell_idx == 0:
            return False
        else:
            return cell_list[cell_idx - 1].row_index != cell_list[cell_idx].row_index

    def __create_table_header(
            self,
            cell: DocumentTableCell 
    ) -> str:
        """Create markdown table header string.

        Args:
            cell:
                Cell data of Azure Document Intelligence result.

        Returns:
            markdown table header string
            example: 

                if plain cell:
                    "<th>HEADER1</th>\n"

                if column span cell:
                    "<th colspan="2">HEADER1</th>\n"
        """

        if (cell.column_span is not None) and (cell.row_span is not None):
            return f"<th colspan=\"{cell.column_span}\" rowspan=\"{cell.row_span}\">{cell.content}</th>\n"
        elif cell.column_span is not None:
            return f"<th colspan=\"{cell.column_span}\">{cell.content}</th>\n"
        elif cell.row_span is not None:
            return f"<th rowspan=\"{cell.row_span}\">{cell.content}</th>\n"
        else:
            return f"<th>{cell.content}</th>\n"

    def __create_table_data(
            self,
            cell: DocumentTableCell 
    ) -> str:
        """Create markdown table data string.

        Args:
            cell:
                Cell data of Azure Document Intelligence result.

        Returns:
            markdown table data string
            example: 

                if plain cell:
                    "<td>data1</td>\n"

                if column span cell:
                    "<td colspan="2">data1</td>\n"
        """

        if (cell.column_span is not None) and (cell.row_span is not None):
            return f"<td colspan=\"{cell.column_span}\" rowspan=\"{cell.row_span}\">{cell.content}</td>\n"
        elif cell.column_span is not None:
            return  f"<td colspan=\"{cell.column_span}\">{cell.content}</td>\n"
        elif cell.row_span is not None:
            return f"<td rowspan=\"{cell.row_span}\">{cell.content}</td>\n"
        else:
            return f"<td>{cell.content}</td>\n"

    def __get_markdown_paragraph(
            self,
            role: str,
            content: str,
            is_first_line: bool
    ) -> str:
        """Create markdown paragraph string.

        Args:
            role:
                Role of the paragraph.
            content:
                paragraph content.
            is_first_line:
                True if the paragraph is the first line, False otherwise.

        Returns:
            markdown paragraph string.
        """

        if (role == 'title') and is_first_line:
            return '# ' + content
        elif (role == 'title') and (not is_first_line):
            return '\n\n# ' + content
        elif role == 'sectionHeading':
            return '\n\n## ' + content
        else:
            return '\n' + content

    def __get_figure_summarize(
            self,
            figure_idx: int,
            analyze_result: AnalyzeResult,
            source_pdf_path: str
    ) -> str:
        """Create markdown paragraph string whitch is summarize of image information.

        Args:
            figure_idx:
                Index of figure in the analyze result.
            analyze_result:
                Azure Document Intelligence result of extracting file.
            source_pdf_path:
                Extracted Source file by Azure Document Intelligence.

        Returns:
            markdown paragraph string whitch is summarize of image information.
        """

        figure = analyze_result.figures[figure_idx]
        tempdir = "./temp"
        if 'boundingRegions' in figure:
            for i, br in enumerate(figure['boundingRegions']):
                page_number = br['pageNumber']
                bbox = br['polygon']
                cordinates = [bbox[0] * 72, bbox[1] * 72, bbox[4] * 72, bbox[5] * 72]
                img = self.img_extractor.extract(source_pdf_path, page_number, tempdir, cordinates)
                img_summary = self.img_summarizer.summarize(img)
                return f'[この部分にはもともと画像情報が添付されていました。画像情報の要約は以下になります。]\n({img_summary})'
