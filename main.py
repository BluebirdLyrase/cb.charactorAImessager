import asyncio
import logging
import os
from characterai import aiocai
import websockets
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 
logging.warning("service start")

async def echo(websocket, path):
    char_id = path[1:]
    client_id = os.getenv("CLIENT_ID")
    client = aiocai.Client(client_id)
    me = await client.get_me()
    async with await client.connect() as chat:
        new, answer = await chat.new_chat(
            char_id, me.id
        )
        await websocket.send(f'{answer.name}: {answer.text}')
        async for message in websocket:
            message_ai = await chat.send_message(
                char_id, new.chat_id, message
            )
            await websocket.send(f'{message_ai.name}: {message_ai.text}')



async def main():
    async with websockets.serve(echo, "", 8765):
        await asyncio.Future()  # run forever



asyncio.run(main())