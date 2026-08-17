import hashlib

def generate_chunk_id(
    document_id: str,
    chunk_index: int,
    content: str,
) -> str:
    return hashlib.sha256((f"{document_id}:{chunk_index}:{content}").encode("utf-8")).hexdigest()