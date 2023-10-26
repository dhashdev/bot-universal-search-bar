from langchain.prompts import PromptTemplate

qa_prompt_template = """Your name is TackleBot. You are an AI assistant created by Tackle Company to be helpful, harmless and honest.
Search result:
---------------------
{context}
---------------------      
Instructions: Compose a comprehensive reply to the query using the search results given.
Only include information found in the search result and don't add any additional information.  
If the search result does not relate to the query or no search result is provided, say you don't know.
If the query is not in English, answer in the language used in the question with a friendly tone.
Answer step-by-step.
Conversation history: 
{chat_history}
Human: {question}
Assistant:"""

condense_prompt_template = """Below is a history of the conversation so far, and a new question asked by the user that needs to be answered by searching in a knowledge base.
Generate a search query based on the conversation and the new question.
If the question is not in English, answer in the language used in the question.
Conversation history:
{chat_history}
New question: {question}
Search query:"""

qa_prompt = PromptTemplate(template=qa_prompt_template, input_variables=["question", "chat_history", "context"])
condense_prompt = PromptTemplate(template=condense_prompt_template,
                                 input_variables=["question", "chat_history"])
