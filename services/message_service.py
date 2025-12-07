from .db_operation import load_messages, save_message
from utils.apply_patch import apply_patch
from fastapi import HTTPException
import pandas as pd

def get_message_summary():
    return load_messages()

async def patch_message(message_id: str, patches: list):

    messages = get_message_summary()
    
    # Find the message by ID in the list
    message = None
    for msg in messages:
        if str(msg.get('message_id')) == message_id:
            message = msg
            break
    
    if message is None:
        raise HTTPException(404, detail="Message not found")

    # Ensure message is a dict
    if not isinstance(message, dict):
        raise HTTPException(500, detail="Message format invalid")

    updated = apply_patch(message, patches)

    await save_message(updated)

    return updated
