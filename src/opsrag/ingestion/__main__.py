from opsrag.ingestion.pipeline import ingest_directory
from pathlib import Path
from collections import Counter

def main() -> None:
    knowledge_base_path = Path(__file__).resolve().parent.parent.parent.parent / "knowledge-base"

    result = ingest_directory(knowledge_base_path)

    domain_counter = Counter(document.domain or "unknown" for document in result.documents)
    type_counter = Counter(document.file_type for document in result.documents)

    type_count = "\n".join(
    f"{key}: {type_counter[key]}"
    for key in sorted(type_counter)
)

    domain_count = "\n".join(
    f"{key}: {domain_counter[key]}"
    for key in sorted(domain_counter)
)

    print("OpsRAG Ingestion")
    print()

    print(f"Discovered: {len(result.documents) + len(result.errors)}")
    print(f"Processed: {len(result.documents)}")
    print(f"Failed: {len(result.errors)}")
    print()

    print("By type:")
    for key in sorted(type_counter):
        print(f"  {key}: {type_counter[key]}")

    print()

    print("By domain:")
    for key in sorted(domain_counter):
        print(f"  {key}: {domain_counter[key]}")

if __name__ == "__main__":
    main()