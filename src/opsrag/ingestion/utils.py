import hashlib

def generate_document_id(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()