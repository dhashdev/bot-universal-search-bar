import PyPDF2
from langchain.docstore.document import Document


class PDFLoader:
    def __init__(self, user_id, file_name, file_path):
        self.user_id = user_id
        self.file_name = file_name
        self.file_path= file_path

    def load(self):
        pdftext = ""
        with open(self.file_path, "rb") as pdfFileObj:
            pdf_reader = PyPDF2.PdfReader(pdfFileObj)
            for page in pdf_reader.pages:
                pdftext += page.extract_text()
        return [Document(page_content=pdftext, metadata={"user_id": self.user_id, "source": self.file_name})]
