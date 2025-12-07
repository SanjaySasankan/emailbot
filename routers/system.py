from fastapi import APIRouter, HTTPException


router = APIRouter(prefix="/system", tags=["System"])

@router.get("/alive")
def alive():
    return {"status": "alive"} 
