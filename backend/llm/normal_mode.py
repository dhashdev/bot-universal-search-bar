from utils.tools import GoogleSearchHandler
from .base_chain import BaseChain
from config.settings import settings
from prompts import (decision_human_prompt, decision_system_prompt,
                     web_search_system_prompt, web_search_human_prompt,
                     simple_qna_system_prompt, simple_qna_human_prompt)

class AnswerPredictor:
    def __init__(self):
        self.decision_chain = BaseChain(decision_system_prompt, decision_human_prompt)
        self.simple_qna_chain = BaseChain(simple_qna_system_prompt, simple_qna_human_prompt)
        self.web_search_chain = BaseChain(web_search_system_prompt, web_search_human_prompt)
        self.search_tools = GoogleSearchHandler(google_api_key=settings.search_api.GOOGLE_API_KEY, google_cse_id=settings.search_api.GOOGLE_CSE_ID)

    def predict(self, question: str, history: str):
        decision = self.make_decision(question)
        if "LLM Model" in decision:
            return self.predict_without_search(question, history)
        return self.predict_with_search(question, history)

    def make_decision(self, question: str) -> str:
        return self.decision_chain.predict(question=question)
    
    def predict_without_search(self, question: str, history: str):
        return self.simple_qna_chain.predict(question=question, history=history), ""
    
    def predict_with_search(self, question: str, history: str):
        reference_results, display_append = self.search_tools.get_results(question, history, top_k=10)
        context_data = "\n\n".join(reference_results)
        return self.web_search_chain.predict(context=context_data, question=question, history=history), display_append
