# https://app.pinecone.io/organizations/-NZRbmS1JEhANi1-NvGD/projects/us-west1-gcp-free:fee66f6/keys
class PineconeSettings:
    PINECONE_API_KEY = "82b9902a-2908-4ece-88bf-483c413a91d7"
    PINECONE_ENVIRONMENT = "us-west1-gcp-free"
    INDEX_NAME = "text-indexing"
    NAME_SPACE_1 = "documents"


class CosmosDBSettings:
    CREDENTIAL = "RtzkEq11S4Q036EUdgBfiyNJ8xI3bd46FHGiJ43Ru2nxu6IeTcIsmjKJ5Nf8QO5rfUmnWfAN0yHKACDbKf5LYQ=="
    ENDPOINT = 'https://tacklebot.documents.azure.com:443/'
    DATABASE = "chatgpt"
    CONTAINER_COSMOS = "history"
