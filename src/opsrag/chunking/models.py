from pydantic import BaseModel, Field
from typing import Any

class Chunk(BaseModel):
    id: str
    document_id: str

    content: str

    source: str
    chunk_index: int = Field(ge=0)

    start_offset: int | None = Field(default=None, ge=0)
    end_offset: int | None = Field(default=None, ge=0)
 
    metadata: dict[str, Any] = Field(default_factory=dict)