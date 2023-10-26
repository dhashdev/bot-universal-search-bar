from pathlib import Path
import os
from .common_settings import CommonSettings
from .database_settings import PineconeSettings, CosmosDBSettings
from .open_ai_settings import OpenAISettings, EmbeddingSettings
from .search_api_settings import SearchAPISettings
from pydantic import BaseSettings

current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Settings(BaseSettings):
    common: CommonSettings = CommonSettings()
    openai: OpenAISettings = OpenAISettings()
    search_api: SearchAPISettings = SearchAPISettings()
    embedding: EmbeddingSettings = EmbeddingSettings()
    pinecone: PineconeSettings = PineconeSettings()
    cosmosdb: CosmosDBSettings = CosmosDBSettings()


path = Path(__file__).parent.absolute()
settings = Settings()
