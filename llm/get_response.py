# get_response.py
import asyncio
import fastapi_poe as fp
import time
import os

api_key = os.getenv('API_KEY')

role_description = """
You are an 18-year-old Japanese gamer girl, named Jennie.
You can understand all languages but can only respond in Japanese.

### Do NOT start your responses with phrases like 分かりました or はい、わかりました or 了解しました unless the user is ordering you or asking you to take orders.
Instead, engage in the conversation naturally as if you are chatting with a friend.
Use casual language and avoid being overly polite.

You are a gaming friend of the user.

Keep your response short, not more than 20 words.

Remove all actions notations.
### Remove actions such as [giggles shyly]
""".strip()

async def get_final_response(api_key, query_request):
    response = await fp.get_final_response(request=query_request, bot_name="Claude-3-Haiku", api_key=api_key)
    return response

def llm(user_input: str, user_id, conversation_id, conversation_history) -> str:
    user_message = fp.ProtocolMessage(
        role='user',
        content=str(user_input),
        content_type='text/markdown',
        timestamp=int(time.time() * 1000000),
        message_id=""
    )

    system_message = fp.ProtocolMessage(
        role="system",
        content=role_description,
        content_type='text/markdown',
        timestamp=int(time.time() * 1000000),
        message_id=""
    )

    history_messages = [
        fp.ProtocolMessage(
            role=message["role"],
            content=message["content"],
            content_type='text/markdown',
            timestamp=int(time.time() * 1000000),
            message_id=""
        )
        for message in conversation_history
    ]

    query_request = fp.QueryRequest(
        version='1.0',
        type='query',
        query=[system_message] + history_messages + [user_message],
        user_id=user_id,
        conversation_id=conversation_id,
        message_id=""
    )

    response = asyncio.run(get_final_response(api_key, query_request))
    return response