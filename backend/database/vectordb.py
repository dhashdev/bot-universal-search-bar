import pinecone
from langchain.embeddings import OpenAIEmbeddings
from .custom_pinecone import Pinecone
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class VectorStore:

    def __init__(self):
        self.index_name = settings.pinecone.INDEX_NAME
        self.namespace = settings.pinecone.NAME_SPACE_1

        pinecone.init(
            api_key=settings.pinecone.PINECONE_API_KEY,
            environment=settings.pinecone.PINECONE_ENVIRONMENT
        )

        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.embedding.EMBEDDINGS_KEY,
            chunk_size=16
        )

        if self.index_name not in pinecone.list_indexes():
            self.create_index()

        self.index = pinecone.Index(self.index_name)

    def create_index(self):
        pinecone.create_index(
            self.index_name,
            metric="cosine",
            dimension=1536
        )
        logger.info(f"Index {self.index_name} created successfully")

    def delete_document(self, user_id, doc_id):
        filter = {
            "source": {"$in": [doc_id]},
            "user_id": {"$eq": user_id}
        }
        self.index.delete(filter=filter, namespace=self.namespace)
        logger.info(f"Deleted {doc_id} successfully")

    def upload_document(self, documents):
        Pinecone.from_documents(documents, self.embeddings, index_name=self.index_name, namespace=self.namespace)

    def load(self):
        return Pinecone.from_existing_index(
            self.index_name,
            self.embeddings,
            namespace=self.namespace
        )
