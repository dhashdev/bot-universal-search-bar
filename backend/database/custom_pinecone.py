from langchain.vectorstores import Pinecone as PineconeLangChain
from typing import List, Tuple, Any
from langchain.docstore.document import Document


class Pinecone(PineconeLangChain):
    def similarity_search_with_relevance_scores(
            self,
            query: str,
            k: int = 4,
            **kwargs: Any,
    ) -> List[Tuple[Document, float]]:
        return [
            a
            for a in self.similarity_search_with_score(query, k=k)
            if a[1] > kwargs["score_threshold"]
        ]
