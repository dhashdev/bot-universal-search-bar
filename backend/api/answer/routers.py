from fastapi import APIRouter, Form, Query, HTTPException
from typing import List, Tuple, Optional
from config.settings import settings
from langchain.chat_models import AzureChatOpenAI, ChatOpenAI
from database.vectordb import VectorStore
from database.cosmosdb import CosmosDB
from prompts import qa_prompt, condense_prompt
from llm import CustomConversationalRetrievalChain, AnswerPredictor, BaseChain
# from prompts import create_topic_human_prompt, create_topic_system_prompt
from utils.helper import process_history, add_details
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Chat bot"], prefix="/api/answer")

vectordb = VectorStore()
cosmosdb = CosmosDB()


@router.post("/chat-docs")
def answer_with_docs(
        question: str = Form(...),
        user_id: str = Form(...),
        conversation_id: str = Form(...)
):
    try:
        llm = ChatOpenAI(
            openai_api_key=settings.openai.API_KEY,
            temperature=0.,
            streaming=False
        )

        vectorstore = vectordb.load()

        qa = CustomConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(
            search_kwargs={'filter': {'user_id': user_id}}),
                                                         condense_question_llm=llm, verbose=True,
                                                         condense_question_prompt=condense_prompt,
                                                         combine_docs_chain_kwargs={"prompt": qa_prompt},
                                                         return_source_documents=True,
                                                         get_chat_history=lambda h: h)
        # query with input and chat history
        items = cosmosdb.read_item(user_id, conversation_id)

        converted_data = [[item["prompt"], item["response"]] for item in items["queries"]]
        history_template = process_history(converted_data[-2:])
        response = qa({"question": question, "chat_history": history_template})

        relevant_docs = response["source_documents"]
        display_append = ""

        if relevant_docs:
            reference_results = [d.page_content for d in relevant_docs]
            reference_sources = [d.metadata["source"] for d in relevant_docs]
            display_append = add_details(reference_results, reference_sources)
            display_append = "\n".join(display_append)

        result = {"answer": response['answer'], "sources": display_append}
        logger.debug(result)

        items['queries'].append({
            "prompt": question,
            "response": result["answer"],
            "sources": result['sources']
        })
        cosmosdb.upsert_item(items)
        # else:
        #     # llm_topic = BaseChain(create_topic_system_prompt, create_topic_human_prompt)
        #     # conversation_name = llm_topic.predict(inputs = question, outputs = result["answer"])
        #     conversation_id = cosmosdb.create_item(question, conversation_name, result)

        result["conversation_id"] = str(conversation_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/new_conversation")
def create_conversation(user_id: str = Form(...), name: str = Form(...)):
    try:
        conversation_id = cosmosdb.create_item(user_id, name)
        return {"name": name, "id": conversation_id}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/chat")
def answer(question: str, user_id: str, conversation_id: Optional[str] = None):
    try:
        llm_chain = AnswerPredictor()
        items = cosmosdb.read_item(user_id, conversation_id)
        converted_data = [[item["prompt"], item["response"]] for item in items["queries"]]

        response, sources = llm_chain.predict(question, converted_data[-2:])

        result = {"answer": response, "sources": sources}
        logger.debug(result)

        items['queries'].append({
            "prompt": question,
            "response": result["answer"],
            "sources": result['sources']
        })
        cosmosdb.upsert_item(items)

        result["conversation_id"] = str(conversation_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
