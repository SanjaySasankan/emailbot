from fastapi import APIRouter, HTTPException
from services.analytics_service import (
    get_team_summary,
    get_users_summary,
    get_user_report,
    aggregate_user_sentiment
)
from services.message_service import get_message_summary as get_messages

router = APIRouter(prefix="/reports", tags=["Front"])

@router.get("/team")
def team_report():
    return get_team_summary()

@router.get("/users")
def users_report():
    return get_users_summary()

@router.get("/user/{id}")
def user_report(user_id: str):
    data = get_user_report(user_id)
    if not data:
        raise HTTPException(404, detail="User not found")
    return data

@router.get("/aggregate-sentiment")
def aggregated_report():
    data = aggregate_user_sentiment()
    # Handle None or empty DataFrame explicitly to avoid ambiguous truth value
    if data is None:
        raise HTTPException(500, detail="Failed to aggregate sentiment")
    if hasattr(data, "empty") and data.empty:
        return []

    # Return as list-of-dicts so FastAPI serializes it to JSON properly
    if hasattr(data, "to_dict"):
        return data.to_dict(orient="records")

    return data

