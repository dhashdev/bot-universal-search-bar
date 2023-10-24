from typing import Any, Dict, List, Optional

from langchain.chains import ConversationalRetrievalChain
from langchain.schema import BaseRetriever, Document

class CustomConversationalRetrievalChain(ConversationalRetrievalChain):
    retriever: BaseRetriever
    """Index to connect to."""
    max_tokens_limit: Optional[int] = None
    def _get_docs(
        self,
        question: str,
        inputs: Dict[str, Any]
    ) -> List[Document]:
        """Get docs."""
        docs = self.retriever.get_relevant_documents(
            question
        )
        # Add attribute to docs call docs.citation
        for (idx, d) in enumerate(docs):
            item = [d.page_content.strip("�"), d.metadata["source"]]
            d.page_content = f'[{idx+1}] {item[0]}'
            d.metadata["source"] = f'{item[1]}'
        return self._reduce_tokens_below_limit(docs)