"""
基于openpyxl
https://openpyxl.readthedocs.io/en/stable/index.html
"""
import os
from pathlib import Path

from openpyxl import Workbook, load_workbook

BASE_DIR = Path(__file__).resolve().parent.parent


class XlsxTools:
    file_path = ''
    file_name = ''

    def load_file(self, file_path):
        return load_workbook(file_path)
