# Architecture

## Overview

OpsRAG follows a Retrieval-Augmented Generation architecture focused on operational incident investigation.

The system retrieves relevant information from an internal knowledge base, ranks the retrieved evidence, builds a context for the LLM, and generates a structured diagnosis.

```text
Operational Knowledge
Runbooks / Postmortems / Terraform / YAML / Logs
                         │
                         ▼
                  Ingestion Pipeline
                         │
                         ▼
                 Parsing + Chunking
                         │
                         ▼
                Metadata Enrichment
                         │
                         ▼
        PostgreSQL + pgvector + Full Text Search
                         │
                         ▼
                  Query Processing
                         │
                         ▼
                 Hybrid Retrieval
                         │
                         ▼
                     Reranker
                         │
                         ▼
                Context Construction
                         │
                         ▼
                        LLM
                         │
                         ▼
          Diagnosis + Evidence + Citations
```

---

## Main Components

### Knowledge Base

The initial knowledge base will contain operational documents related to the three MVP use cases:

- Kafka high CPU
- Lambda to SNS timeout
- EKS to RDS timeout

Supported document types will initially include:

- Markdown
- plain text
- JSON
- YAML
- Terraform
- logs

The first version will use synthetic or sanitized data and will not connect directly to production systems.

---

### Ingestion Pipeline

The ingestion pipeline will:

1. discover documents
2. parse their content
3. normalize them into a common representation
4. split them into chunks
5. attach metadata
6. generate embeddings
7. store the results

Example metadata:

```json
{
  "service": "kafka",
  "environment": "production",
  "document_type": "runbook",
  "incident_type": "high_cpu",
  "source": "kafka/runbooks/high-cpu.md"
}
```

The pipeline should eventually support reprocessing modified documents wihtout duplicating unchanged content.

---

### Storage

PostgreSQL will be the main datastore.

It will store:

- documents
- chunks
- metadata
- embeddings
- query traces
- evaluation results

`pgvector` will be used for vector similarity search.

PostgreSQL Full Text Search will provide keyword-based retrieval.

Using the same database for structured data, metadata, vector search, and keyword search keeps the initial architecture simple.

---

## Retrieval Pipeline

The retrieval pipeline will combine semantic and lexical search.

```text
User Question
      │
      ▼
Query Processing
      │
      ├───────────────┐
      ▼               ▼
Vector Search     Keyword Search
      │               │
      └───────┬───────┘
              ▼
        Result Fusion
              │
              ▼
         Metadata Filters
              │
              ▼
           Reranker
              │
              ▼
        Top Relevant Chunks
```

### Vector Search

Embeddings will be used to retrieve documents that are semantically similar to the user's question.

This is useful when the wording of the questions differs from the wording used in the documentation.

### Keyword Search

Keyword search will complement embeddings for technical values such as:

- error codes
- resource names
- ports
- AWS services
- Kubernetes objects
- configuration keys

Example:

```text
ETIMEDOUT
5432
prod-kafka-0
sns:Publish
```

### Hybrid Retrieval

Vector and keyword results will be combined before reranking.

This should improve retrieval quality compared with using vector search alone.

The effectiveness of this approach will later be measure during evaluation phase.

---