# get_response.py
import asyncio
import fastapi_poe as fp
import time
import os
from llm.role_desc import role_description
api_key = os.getenv('API_KEY')



async def get_final_response(api_key, query_request):
    response = await fp.get_final_response(request=query_request, bot_name="Claude-3-Haiku", api_key=api_key)
    return response


def llm(user_input: str, user_id, conversation_id, conversation_history) -> str:
    # Format conversation history into a structured conversation
    formatted_messages = []
    
    # Add system message first
    formatted_messages.append(
        fp.ProtocolMessage(
            role='system',
            content=role_description,
            content_type='text/markdown',
            timestamp=int(time.time() * 1000000),
            message_id=""
        )
    )
    
    # Add conversation history
    for msg in conversation_history:
        formatted_messages.append(
            fp.ProtocolMessage(
                role=msg['role'],
                content=msg['content'],
                content_type='text/markdown',
                timestamp=int(time.time() * 1000000),
                message_id=""
            )
        )
    
    # Add current user message
    formatted_messages.append(
        fp.ProtocolMessage(
            role='user',
            content=str(user_input),
            content_type='text/markdown',
            timestamp=int(time.time() * 1000000),
            message_id=""
        )
    )
    
    query_request = fp.QueryRequest(
        version='1.0',
        type='query',
        query=formatted_messages,
        user_id=user_id,
        conversation_id=conversation_id,
        message_id="",
    )

    response = asyncio.run(get_final_response(api_key, query_request))
    return response