import asyncio
import json
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
        async for inp in websocket:
            json_input = json.loads(inp)
            # logging.warning(json_input)
            message_ai = await chat.send_message(
                char_id, new.chat_id, json_input['message']
            )
            logging.info(message_ai)
            output = json.dumps({
                    "message":message_ai.text,
                    "channelID":json_input['channelID']
                })
            await websocket.send(output)



async def main():
    async with websockets.serve(echo, "", 8765):
        await asyncio.Future()  # run forever



asyncio.run(main())