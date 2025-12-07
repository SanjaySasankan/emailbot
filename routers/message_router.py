from fastapi import APIRouter, HTTPException
from models.patch_model import PatchRequest
from services.message_service import get_message_summary as get_messages
from services.message_service import patch_message as patch


router = APIRouter(prefix="/reports", tags=["Snowflake"])

@router.get("/messages")
def user_messages():
    return get_messages()


@router.patch("/{id}")
async def update_message(message_id: str, patches: PatchRequest):
    """
    JSON Patch endpoint for messages.
    Accepts a list of operations.
    """
    # Extract the root list of patch operations from RootModel
    patch_operations = patches.root if hasattr(patches, 'root') else patches
    updated = await patch(message_id, patch_operations)
    return {"message_id": message_id, "updated": updated}