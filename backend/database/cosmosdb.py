from azure.cosmos import CosmosClient, PartitionKey
from datetime import date, datetime
import uuid
from typing import Dict, List, Any
from config.settings import settings


class CosmosDB:

    def __init__(self):
        self.client = CosmosClient(url=settings.cosmosdb.ENDPOINT, credential=settings.cosmosdb.CREDENTIAL)
        self.database = self.client.create_database_if_not_exists(settings.cosmosdb.DATABASE)
        self.container = self.database.create_container_if_not_exists(
            settings.cosmosdb.CONTAINER_COSMOS,
            partition_key=PartitionKey("/user_id")
        )

    @staticmethod
    def serialize_datetime(obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    def create_item(self, user_id: str, name: str) -> str:
        response = self.container.create_item(
            body={
                "user_id": user_id,
                "id": str(uuid.uuid4()),
                "date": self.serialize_datetime(datetime.utcnow()),
                "name": name,
                "queries": []
            }
        )
        return response["id"]

    def upsert_item(self, items: List[Dict]):
        items['date'] = self.serialize_datetime(datetime.utcnow())
        self.container.upsert_item(
            body=items
        )

    def replace_item(self, query: str = None, parameters: List[Dict] = None, new_name: str = None):
        items = self.query_item(query=query, parameters=parameters)
        if items:
            item = items[0]
            item["name"] = new_name
            self.container.replace_item(item, item)

    def query_item(self, query: str = None, parameters: List[Dict] = None):
        if parameters is None:
            items = list(self.container.query_items(query=query, enable_cross_partition_query=True))
        else:
            items = list(
                self.container.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))
        return items

    def read_item(self, user_id: str, conversation_id: str):
        return self.container.read_item(item=conversation_id, partition_key=user_id)

    def delete_item(self, user_id: str, conversation_id: str):
        self.container.delete_item(item=conversation_id, partition_key=user_id)
        return f"Delete {conversation_id} successfully"
