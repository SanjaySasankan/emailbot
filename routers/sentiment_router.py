from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from models.patch_model import PatchOperation
from services.message_service import get_message_summary, patch_message
from services.sentiment_service import mock_sentiment_analyzer

router = APIRouter(prefix="/sentiment", tags=["Sentiment"])

# # SINGLE MESSAGE ANALYSIS
# @router.get("/analyze/{message_id}")
# def analyze_message_by_id(message_id: str):
#     pass

# BULK ANALYSIS
class BulkSentimentRequest(BaseModel):
    messages: List[str] = None

@router.post("/bulk-analyze")
async def bulk_analyze():
    results = []

    messages = get_message_summary()
    outbound_messages = [msg for msg in messages if msg['direction'] == 'outbound']
    for msg in outbound_messages:
        if not msg['analyzed']:
            sentiment = mock_sentiment_analyzer(msg['body'])
            await patch_message(str(msg['message_id']), [
                PatchOperation(op="replace", path="/tone", value=sentiment['tone']),
                PatchOperation(op="replace", path="/sentiment", value=sentiment['sentiment']),
                PatchOperation(op="replace", path="/score", value=sentiment['score']),
                PatchOperation(op="replace", path="/emotion", value=sentiment['emotion']),
                PatchOperation(op="replace", path="/analyzed", value=True),
            ])
            results.append(sentiment)

    return {"count": len(results), "results": results}
