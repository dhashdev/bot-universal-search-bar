from langchain.utilities.google_search import GoogleSearchAPIWrapper
from llm import BaseChain
from prompts import condense_web_human_prompt, condense_web_system_prompt
from .helper import add_source_numbers

class GoogleSearchHandler:
    def __init__(self, google_api_key, google_cse_id):
        self.search = GoogleSearchAPIWrapper(google_api_key=google_api_key, google_cse_id=google_cse_id)
        self.llm_chain = BaseChain(condense_web_system_prompt, condense_web_human_prompt)

    def get_results(self, inputs: str, history: str, top_k=6):
        results = self.search.results(self.llm_chain.predict(question=inputs, history=history), num_results=top_k)

        reference_results = []
        display_append = []

        for idx, result in enumerate(results):
            reference_results.append([result['snippet'], result['link']])
            display_append.append(f'<a href=\"{result["link"]}\" target=\"_blank\">{idx + 1}.&nbsp;{result["title"]}</a>')
        reference_results = add_source_numbers(reference_results)
        return reference_results, "\n".join(display_append)
