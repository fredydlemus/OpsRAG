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

## Reranking

The first retrieval step will return a larger number of candidate chunks.

A reranker will then assign a more precise relevance score and select the best evidence for the final context.

```text
Hybrid Retrieval
      │
      ▼
20 candidate chunks
      │
      ▼
Reranker
      │
      ▼
5–8 final chunks
```

This reduces irrelevant context and helps prevent the LLM from receiving too much noisy information.

## Context Construction

The context builder will prepare the retrieved evidence before sending it to the LLM.

Responsibilities include:

- removing duplicate information
- preserving source references
- respecting context limits
- prioritizing highly ranked chunks
- maintaining document metadata

The LLM should receive only the evidence necessary to investigate the question.

---

## Generation

The LLM will generate a structured diagnostic response.

The response should contain:

- summary
- observed facts
- hypotheses
- supporting evidence
- recommended checks
- limitations
- source citations

Example:

```json
{
  "summary": "The Kafka broker is operating close to its CPU limit.",
  "hypotheses": [
    {
      "cause": "JMX metrics overhead",
      "confidence": 0.78,
      "evidence": [
        {
          "source": "kafka/metrics/jmx-analysis.md"
        }
      ]
    }
  ],
  "recommended_checks": [],
  "limitations": []
}
```

The final schema will be implemented when the generation layer is built.

---

## Traceability

Each query should eventually produce a trace containing:

```text
Original Question
        ↓
Processed Query
        ↓
Retrieved Chunks
        ↓
Retrieval Scores
        ↓
Reranking Scores
        ↓
Context Sent to LLM
        ↓
Generated Response
```

This will make it possible to understand whether an incorrect answer was caused by:

- retrieval
- ranking
- context construction
- generation

Traceability will also support evaluation and debugging.

---

## Backend Architecture

The application backend will use:

- Python
- FastAPI
- Pydantic

The main modules are expected to evolve toward a structure similar to:

```text
src/opsrag/
├── ingestion/
├── chunking/
├── embeddings/
├── retrieval/
├── reranking/
├── generation/
├── evaluation/
└── api/
```

The exact structure will evolve during implementation.

---

## Local Development

The local environment will use Docker Compose.

Initial services are expected to include:

```text
Docker Compose
├── OpsRAG API
└── PostgreSQL + pgvector
```

External LLM and embeddings APIs may initially be accessed directly from the backend.

This keeps the local architecture simple while the RAG pipeline is being developed.

---

## AWS Deployment

The final cloud architecture will be defined after the local implementation is stable.

A likely deployment architecture is:

```text
Client
  │
  ▼
Frontend
  │
  ▼
FastAPI
  │
  ├── RDS PostgreSQL + pgvector
  ├── S3
  ├── LLM / Embedding Provider
  └── Observability
```

Infrastructure will be managed using Terraform.

The exact compute platform, such as ECS or EKS, will be decided later based on the needs of the application rather than being selected upfront.

---

## Key Architecture Decisions

### PostgreSQL + pgvector

Chosen to keep structured data, metadata, vector search, and full-text search in a single system during the MVP.

### Hybrid Retrieval

Chosen because operational queries frequently combine semantic concepts with exact technical terms.

### Reranking

Included to improve the quality of the final context before generation.

### Structured Responses

The LLM output will be validated rather than returned as unrestricted text.

### Evidence-Based Answers

Environment-specific conclusions should be linked to retrieved sources.

### No Autonomous Actions

The MVP will investigate incidents but will not execute operational commands or modify infrastructure.

### Evaluation Before Complexity

Advanced techniques sush as agents or GraphRAG will only be considered if evaluation results show a clear need.

---

## Initial Architecture Goal

The first implementation target is intentionally simple:

```text
Documents
   ↓
Ingestion
   ↓
Chunks
   ↓
Embeddings
   ↓
PostgreSQL + pgvector
   ↓
Semantic Search
   ↓
LLM
```

From that baseline, OpsRAG will evolve incrementally toward:

```text
Hybrid Retrieval
      +
Reranking
      +
Structured Generation
      +
Evaluation
      +
Observability
```

Each additional component should be justified by measurable improvements rather than added only for architectural complexity.