from langchain.docstore.document import Document
from langchain.document_loaders import CSVLoader as loader

class CSVLoader:
    def __init__(self, user_id, file_name, file_path):
        self.user_id = user_id
        self.file_name = file_name
        self.file_path= file_path

    def load(self):
        _loader = loader(self.file_path, encoding="utf8")
        documents = _loader.load()
        for doc in documents:
            doc.metadata['user_id'] = self.user_id

        return documents
