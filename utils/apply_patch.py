from fastapi import HTTPException
from models.patch_model import PatchOperation

def apply_patch(original: dict, patches: list[PatchOperation]):
    """
    Applies JSON Patch operations (replace only for now).
    """
    for patch in patches:
        op = patch.op
        path = patch.path
        value = patch.value

        # Remove leading slash in path
        field = path.lstrip("/")

        if field not in original:
            raise HTTPException(400, detail=f"Field '{field}' not found in message")

        if op == "replace":
            original[field] = value

    return original