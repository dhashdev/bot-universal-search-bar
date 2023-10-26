import os
from langchain.document_loaders import UnstructuredWordDocumentLoader, UnstructuredPowerPointLoader,  TextLoader
from .csv_parser import CSVLoader
from .pdf_parser import PDFLoader


def choose_loader(user_id, file_name, file_path):
    file_type = os.path.splitext(file_name)[1]
    if file_type == ".pdf":
        return PDFLoader(user_id, file_name, file_path)
    elif file_type == ".docx":
        return UnstructuredWordDocumentLoader(file_path)
    elif file_type == ".pptx":
        return UnstructuredPowerPointLoader(file_path)
    elif file_type == '.csv':
        return CSVLoader(user_id, file_name, file_path)
    else:
        return TextLoader(file_path, "utf8")