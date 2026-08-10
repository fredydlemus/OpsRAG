import hashlib

def generate_document_id(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()

def calculate_checksum(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()