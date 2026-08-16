from typing import Any
from pydantic import BaseModel, Field

class Document(BaseModel):
    id: str
    content: str

    source: str
    file_name: str
    file_type: str

    domain: str | None = None
    document_type: str | None = None
    environment: str | None = None
    service: str | None = None
    status: str | None = None

    checksum: str

    metadata: dict[str, Any] = Field(default_factory=dict)

class IngestionError(BaseModel):
    source: str
    error: str

class IngestionResult(BaseModel):
    documents: list[Document] = Field(default_factory=list)
    errors: list[IngestionError] = Field(default_factory=list)