decision_system_prompt = \
"""\
You are an AI assistant that helps people find information."""

decision_human_prompt = \
"""\
Based on the user query, decide on what source to use. Your possible sources are given below:                                              
1. LLM Model: Useful for answering conversational queries and for queries that you can fully answer with your available knowledge.                                              
2. Google Web Search: Useful when the query involves time-sensitive information, recent developments, or unclear queries.                                            
Please answer only the source used as "LLM Model" or "Google Web Search" and nothing else.                              
User: {question}
Begin!"""