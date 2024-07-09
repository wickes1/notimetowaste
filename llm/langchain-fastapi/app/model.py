import hashlib
from typing import Optional

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    page_content: str
    metadata: Optional[dict[str, str]] = {}


class DocumentModel(BaseModel):
    page_content: str
    metadata: Optional[dict[str, str]] = {}

    def generate_digest(self):
        return hashlib.sha256(self.page_content.encode()).hexdigest()
