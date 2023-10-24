from langchain import LLMChain

from backend.config.settings import settings
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


class BaseChain:
    def __init__(self, system_prompt_template: str = "", human_prompt_template: str = "", temperature: float = 0., **model_kwargs):
        self.llm = AzureChatOpenAI(
            deployment_name=settings.openai.AZURE_DEPLOYMENT_NAME,
            openai_api_key=settings.openai.API_KEY,
            openai_api_base=settings.openai.OPENAI_API_BASE,
            openai_api_version=settings.openai.OPENAI_API_VERSION,
            temperature=temperature,
            **model_kwargs
        )
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt_template),
            HumanMessagePromptTemplate.from_template(human_prompt_template)
        ])
        self.llm_chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def predict(self, **kwargs) -> str:
        prediction = self.llm_chain.predict(**kwargs)
        
        return prediction
