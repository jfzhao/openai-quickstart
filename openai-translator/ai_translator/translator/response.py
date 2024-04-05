import os
from reportlab.lib import colors, pagesizes, units
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

from book import Book, ContentType
from utils import LOG

class Response:
    def __init__(self):
        pass

    def response_translated_book(self, book: Book, output_file_path: str = None, file_format: str = "TXT") -> str:
        if file_format.lower() == "txt":
            return self._response_translated_book_txt(book, output_file_path)
        elif file_format.lower() == "markdown":
            return self._response_translated_book_markdown(book, output_file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")

    def _response_translated_book_txt(self, book: Book, output_file_path: str = None) -> str:
        if output_file_path is None:
            output_file_path = book.pdf_file_path.replace('.pdf', f'_translated.pdf')

        LOG.info(f"pdf_file_path: {book.pdf_file_path}")
        LOG.info(f"开始翻译: {output_file_path}")

        response = ""

        # Iterate over the pages and contents
        for page in book.pages:
            for content in page.contents:
                if content.status:
                    if content.content_type == ContentType.TEXT:
                        # Add translated text to the PDF
                        text = content.translation
                        response = response + text + '\n\n'

                    elif content.content_type == ContentType.TABLE:
                        # Add table to the PDF
                        table = content.translation
                        response = response + table.to_string()

        LOG.info(f"翻译完成")
        return response

    def _response_translated_book_markdown(self, book: Book, output_file_path: str = None) -> str:
        if output_file_path is None:
            output_file_path = book.pdf_file_path.replace('.pdf', f'_translated.md')

        LOG.info(f"pdf_file_path: {book.pdf_file_path}")
        LOG.info(f"开始翻译: {output_file_path}")
        response = ""
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            # Iterate over the pages and contents
            for page in book.pages:
                for content in page.contents:
                    if content.status:
                        if content.content_type == ContentType.TEXT:
                            # Add translated text to the Markdown file
                            text = content.translation
                            response = response + text + '\n\n'

                        elif content.content_type == ContentType.TABLE:
                            # Add table to the Markdown file
                            table = content.translation
                            header = '| ' + ' | '.join(str(column) for column in table.columns) + ' |' + '\n'
                            separator = '| ' + ' | '.join(['---'] * len(table.columns)) + ' |' + '\n'
                            # body = '\n'.join(['| ' + ' | '.join(row) + ' |' for row in table.values.tolist()]) + '\n\n'
                            body = '\n'.join(['| ' + ' | '.join(str(cell) for cell in row) + ' |' for row in table.values.tolist()]) + '\n\n'
                            response = response + header + separator + body

        LOG.info(f"翻译完成")
        return response