create_topic_system_prompt = "You are an AI assistant created by Tackle Company to be helpful, harmless and honest."

create_topic_human_prompt = """Please create a concise topic (less than 5 words) best suited for the following conversation.
Conversation:
\nUser: {inputs}\nAssistant: {outputs}
Do not include any text inside \"\".
Do not include any special characters like '+'.
Do not generate any text before or after the topic, such as 'Topic:'.
"""