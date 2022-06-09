# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import asyncio
import logging
from ..vars import Var
from pyrogram import Client
from WebStreamer.utils import TokenParser
from . import multi_clients, work_loads, StreamBot


async def initialize_clients():
    multi_clients[0] = StreamBot
    work_loads[0] = 0
    all_tokens = TokenParser().parse_from_env()
    if not all_tokens:
        print("No se encontraron clientes adicionales, utilizando el cliente predeterminado")
        return
    
    async def start_client(client_id, token):
        try:
            print(f"Starting - Client {client_id}")
            if client_id == len(all_tokens):
                await asyncio.sleep(2)
                print("Esto tomará algún tiempo, por favor espere...")
            client = await Client(
                session_name=":memoria:",
                api_id=Var.API_ID,
                api_hash=Var.API_HASH,
                bot_token=token,
                sleep_threshold=Var.SLEEP_THRESHOLD,
                no_updates=True,
            ).start()
            work_loads[client_id] = 0
            return client_id, client
        except Exception:
            logging.error(f"error al iniciar el cliente - {client_id} Error:", exc_info=True)
    
    clients = await asyncio.gather(*[start_client(i, token) for i, token in all_tokens.items()])
    multi_clients.update(dict(clients))
    if len(multi_clients) != 1:
        Var.MULTI_CLIENT = True
        print("Modo Multi-Client habilitado")
    else:
        print("No se inicializaron clientes adicionales, utilizando el cliente predeterminado")
