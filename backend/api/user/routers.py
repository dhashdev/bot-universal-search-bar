from fastapi import APIRouter, HTTPException, Depends, UploadFile, Form, Query
from fastapi.param_functions import File
from typing import List
from pathlib import Path
from config.settings import settings
from file.bulk import choose_loader
from langchain.text_splitter import TokenTextSplitter
import os
from database.vectordb import VectorStore
from database.cosmosdb import CosmosDB

router = APIRouter(tags=["Chat bot"], prefix="/api/user")

vectordb = VectorStore()
cosmosdb = CosmosDB()

text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=30)


def create_user_directory(user: str) -> Path:
    """Creates a directory for a given user if it doesn't exist."""
    save_dir = Path(settings.common.UPLOAD_FOLDER) / user
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir


def save_file(file: UploadFile, save_dir: Path) -> Path:
    """Saves a file to the specified directory."""
    file_path = os.path.join(save_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path


def process_file(user_id: str, filename: str, file_path: Path):
    """Process the file based on its type and return texts."""
    loader = choose_loader(user_id, filename, file_path)
    if not loader:
        return None
    texts = loader.load()
    if len(texts) > 1:
        return texts
    return text_splitter.split_documents(texts)


@router.post("/upload_file")
async def upload_file(user_id: str = Form(...), files: List[UploadFile] = File(...)):
    """Upload a file to get vectorized and indexed."""
    if not user_id:
        raise HTTPException(status_code=400, detail="No user provided.")

    if not files:
        raise HTTPException(status_code=400, detail="No file provided.")

    save_dir = create_user_directory(user_id)
    documents = []

    for file in files:
        file_path = save_file(file, save_dir)
        texts = process_file(user_id, file.filename, file_path)
        if texts:
            documents.extend(texts)

    docs_id = [file.filename for file in files]
    vectordb.upload_document(documents)

    return {"status": "success", "document_id": docs_id}


@router.delete("/delete_file")
async def delete_file(user_id: str, filename: str):
    try:
        file_path = os.path.join(settings.common.UPLOAD_FOLDER, user_id, filename)
        os.remove(file_path)
        vectordb.delete_document(user_id=user_id, doc_id=filename)

        return {"status": "success", "message": f"Deleted {filename} successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/documents")
async def get_documents(user_id: str):
    try:
        files_name = os.listdir(os.path.join(settings.common.UPLOAD_FOLDER, user_id))
        paths = []
        for file_name in files_name:
            paths.append(os.path.join(settings.common.UPLOAD_FOLDER, user_id, file_name))

        return {"status": "success", "documents": files_name, "paths": paths}
    except Exception as e:
        return {"status": "error", "documents": [], "paths": []}


@router.delete("/conversations/{conversation_id}}")
async def delete_conversation(user_id: str, conversation_id: str):
    try:
        message = cosmosdb.delete_item(user_id, conversation_id)
        return {"status": "success", "message": message}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/conversations/{conversation_id}")
async def get_single_conversation(user_id: str, conversation_id: str):
    try:
        conversation = cosmosdb.read_item(user_id, conversation_id)
        return conversation
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/conversations")
async def get_conversations(user_id: str, keyword: str = Query(None)):
    try:
        base_query = f"SELECT * FROM c WHERE c.user_id = '{user_id}'"

        if keyword:
            query = f"{base_query} AND CONTAINS(c.name, '{keyword}') ORDER BY c.date DESC"
        else:
            query = f"{base_query} ORDER BY c.date DESC"

        conversations = cosmosdb.query_item(query=query)
        list_conversations = [{"id": conversation["id"], "name": conversation["name"]} for conversation in
                              conversations]
        return list_conversations

    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/conversations/{conversation_id}")
async def update_conversation_name(conversation_id: str, user_id: str = Form(...), name: str = Form(...)):
    try:
        query = "SELECT * from c WHERE c.id = @id AND c.user_id = @user_id"
        parameters = [
            {"name": "@id", "value": conversation_id},
            {"name": "@user_id", "value": user_id}
        ]
        cosmosdb.replace_item(query=query, parameters=parameters, new_name=name)

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
