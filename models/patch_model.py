from pydantic import BaseModel, RootModel
from typing import List, Any

class PatchOperation(BaseModel):
    op: str
    path: str
    value: Any

class PatchRequest(RootModel):
    root: List[PatchOperation]
