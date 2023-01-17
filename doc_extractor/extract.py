"""
Extractor Module

Extract text content from files such as pdf, docx, txt etc.
"""
import os

import docx2txt
import html2text
from PyPDF2 import PdfReader
from enum import Enum
from tika import parser
import re


class PdfExtractors(Enum):
    """
    Enum class for pdf extractors
    """
    PDFREADER = 'PDFREADER'
    TIKA = 'TIKA'


def get_file_ext(filepath: str) -> str:
    """
    Get extension of the file

    :param filepath: path of the paths
    :return: file extension
    """
    split_tup = os.path.splitext(filepath)
    return split_tup[1]


class ExtractTextFromFile:
    """
    Extract text from file
    """

    text: str = ''

    def __init__(self, filepath: str, pdf_extractor: PdfExtractors = PdfExtractors.TIKA):
        self.filepath = filepath
        self.pdf_extractor = pdf_extractor

    def extract(self):
        """
        Extract text from file

        :return: text present in the file
        """

        file_ext = get_file_ext(self.filepath)

        if file_ext == '.pdf':
            self.read_pdf(self.filepath)

        return self

    def read_file(self, filepath: str) -> str:
        """
        Read content from a file

        :param filepath: path to file
        :return: file content
        """

        text = ""
        with open(filepath, 'r') as f:
            text = f.read()

        return text

    def read_pdf(self, filepath: str):
        """
        Extract text from pdf files

        :param filepath: filepath to the pdf file
        :return: text present in pdf
        """
        text = ""

        if self.pdf_extractor == PdfExtractors.PDFREADER:
            reader = PdfReader(filepath)

            for page in reader.pages:
                text += page.extract_text()

            self.text = text.strip()
        elif self.pdf_extractor == PdfExtractors.TIKA:
            parsed = parser.from_file(filepath)
            self.text = parsed["content"]

        return self

    def read_docx(self, filepath: str):
        """
        Extract text from docx files

        :param filepath: filepath to the docx file
        :return: text present in docx file
        """

        self.text = docx2txt.process(filepath)
        return self

    def read_txt(self):
        """
        Extract text from txt file

        :return: text present in txt file
        """

        self.text = self.read_file(self.filepath)

    def read_html(self):
        """
        Extract text from a html file

        :return: text present in html file
        """

        self.text = self.read_file(self.filepath)
        self.text = html2text.html2text(self.text)
        return self

    def clean_text(self):
        """
        Clean text by removing extra spaces, tabs, newlines using regex

        :return: self
        """

        self.text = re.sub(r'\t+', ' ', self.text)
        self.text = re.sub(r'\n\s+', '\n', self.text)

        self.text = self.text.strip()

        return self

    def get_text(self) -> str:
        """
        Get text

        :return: text
        """
        return self.text
