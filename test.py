import asyncio
import fastapi_poe as fp
import time
import uuid
import os

api_key = os.getenv("API_KEY")

# user_id = f"u-{uuid.uuid4().hex}"
# conversation_id = f"c-{uuid.uuid4().hex}"

user_id = 'u-2bb461e36db34b8baeccbe90db7a0fb7'
conversation_id = 'c-d1326ba729cd43a08885394d11126b3f'

async def get_final_response(api_key, query_request):
    response = await fp.get_final_response(request=query_request, bot_name="Claude-3-Haiku", api_key=api_key)
    return response
while True:
    user_message = fp.ProtocolMessage(
            role='user',
            content=str(input("You: ")),
            content_type='text/markdown',
            timestamp=int(time.time() * 1000000),
        )


    query_request = fp.QueryRequest(
        version='1.0',
        type='query',
        query= [user_message],
        user_id=user_id,
        conversation_id=conversation_id,
        message_id="",
    )
    response = asyncio.run(get_final_response(api_key, query_request))
    print(response)