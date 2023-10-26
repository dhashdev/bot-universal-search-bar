condense_web_system_prompt = "You are an AI assistant created by Tackle Company to be helpful, harmless and honest."

condense_web_human_prompt="""\
Below is the history of the conversation so far and a new question posed by a user that needs to be answered by searching the Internet.
Based on the current conversation and question provided by the user, your task is to create only **ONE** different version of the question so that users can get relevant information from the Internet.
If the question is not in English, answer in the language used in the question.
The answer should be arranged in number order list.
Conversation history:
{history}
New question: {question}
Alternative question:"""