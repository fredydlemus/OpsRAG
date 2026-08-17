from opsrag.chunking.utils import generate_chunk_id

def test_should_generate_chunk_id_deterministic():
    assert generate_chunk_id("ABC", "0", "# runbook") == generate_chunk_id("ABC", "0", "# runbook")