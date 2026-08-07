# OpsRAG

**RAG-powered incident investigation for DevOps and Cloud environments.**

OpsRAG is a Retrieval-Augmented Generation system designed to help DevOps, SRE, Cloud, and Platfotm Engineers investigate infrastructure incidents using operational knowledge such as:

- Runbooks
- Postmortems
- Terraform
- Kubernetes manifests
- Logs
- Architecture documentation
- Configure files

Instead of relying only on the general knowledge of an LLM, OpsRAG retrieves relevant evidence from the organization's knowledge base and uses it to generate strcutured, traceable diagnoses.

---

## Why OpsRAG?

During an incident, engineers often need to search through multiple sources of information before forming a hypothesis.

Important context may be distributed across:

- documentation
- infrastructure repositories
- historical incidents
- configuration files
- logs
- operational procedures

Traditional search can struggle when the engineer describes the problem differently from how it appears in the documentation.

A standalone LLM has the opposite problem: it can provide useful general knowledge, but it does not know the specific infrastructure, configuration, or incident history of the environment.

OpsRAG combines both approaches.

```text
Question
↓
Query Processing
↓
Hybrid Retrieval
↓
Reranking
↓
Relevant Operational Context
↓
LLM
↓
Diagnosis + Evidence + Recommended Checks
```

---

## Example

Input:

```text
The Kafka broker prod-kafka-0 is constantly using around 2.5 CPU,
but consumer lag is zero.

What should I investigate?
```

Expected output:

```json
{
  "summary": "The broker is operating close to its configured CPU limit.",
  "hypotheses": [
    {
      "cause": "JMX metrics overhead",
      "confidence": 0.78,
      "evidence": [
        "The metrics endpoint exposes more than 30,000 series."
      ]
    }
  ],
  "recommended_checks": [
    {
      "priority": 1,
      "description": "Check whether the container is being CPU throttled.",
      "risk": "read-only"
    }
  ],
  "limitations": [
    "No JVM CPU profile is available."
  ]
}
```

The goal is not to automatically determine the root cause.

The goal is to help the engineer reduce the investigation space using evidence.

---

## MVP Use Cases

The first version will focus on three operational incidents.

### 1. Kafka High CPU

Investigate a Kafka broker running close to its CPU limit.

Possible areas of investigation:

- CPU throttling
- JMX Exporter overhead
- Prometheus scraping
- Partition distribution
- Producer/request load
- Garbage collection

### 2. Lambda → SNS Timeout

Investigate a Lambda function inside a VPC that can connect to RDS but times out when publishing to SNS.

Possible areas of investigation:

- NAT Gateway
- Route tables
- VPC Endpoints
- Security Groups
- Network ACLs
- DNS
- IAM

### 3. EKS → RDS Timeout

Investigate a Kubernetes workload that cannot connect to PostgreSQL on RDS.

Possible areas of investigation:

- Application configuration
- DNS
- NetworkPolicies
- Security Groups
- Subnets and routes
- RDS configuration

---

## Core Principles

OpsRAG will follow a few important rules.

### Evidence over assumptions

Environment-specific claims should be supported by retrieved evidence.

### Facts and hypotheses are different

The system should clearly distinguish between:

- facts
- hypotheses
- recommendations
- missing information

### Abstention is valid

If the knowledge base does not contain enough evidence, OpsRAG should say so instead of inventing a diagnosis.

### Safe operations

The MVP will recommend diagnostic commands, but it will not execute infrastructure changes.

Read-only checks will be prioritized.

---

## Architecture

```text
Runbooks / Postmortems / YAML / Terraform / Logs
                         │
                         ▼
                  Ingestion Pipeline
                         │
                         ▼
                 Chunking + Metadata
                         │
                         ▼
        PostgreSQL + pgvector + Full Text Search
                         │
                         ▼
                 Hybrid Retrieval
                         │
                         ▼
                     Reranker
                         │
                         ▼
                 Context Builder
                         │
                         ▼
                        LLM
                         │
                         ▼
          Diagnosis + Evidence + Citations
```

---

## Planned Stack

### AI

- LLM provider: configurable
- Embedding model: configurable
- Reranker: configurable

### Backend

- Python
- FastAPI
- Pydantic

### Retrieval

- PostgreSQL
- pgvector
- PostgreSQL Full Text Search

### Infrastructure

- Docker
- Docker Compose
- AWS
- Terraform

### Observability

- OpenTelemetry
- Structured logs
- Retrieval traces
- Token and latency tracking

---

## Project Roadmap

### Phase 1 - Product Definition

Define the problem, MVP use cases, and expected system behavior.

### Phase 2 - Knowledge Base

Create realistic operational documents for the three incident scenarios.

### Phase 3 - Ingestion Pipeline

Parse and normalize Markdown, YAML, JSON, Terraform, and logs.

### Phase 4 - Chunking & Metadata

Implement structure-aware chunking and metadata extraction.

### Phase 5 - Vector Retrieval

Generate embeddings and implement semantic search with pgvector.

### Phase 6 - Hybrid Retrieval

Combine semantich search, keyword search, metadata filters, and result fusion.

### Phase 7 - Reranking

Improve retrieval quality by reranking candidate chunks.

### Phase 8 - RAG Generation

Generate structured diagnoses with evidence and citations.

### Phase 9 - Evaluation

Measure retrieval and generation quality using a golden evaluation dataset.

### Phase 10 - API & UI

Expose OpsRAG through FastAPI and provide an interface to inspect answers and evidence.

### Phase 11 - Observability & Security

Add tracing, cost tracking, prompt-injection defenses, and secret protection.

### Phase 12 - AWS Deployment

Deploy the complete system using Terraform and AWS services.

---

### Evaluation

OpsRAG will be evaluated as a system, not only by manually reviewing LLM answers.

Retrieval metrics will include:

- Recall@K
- Precision@K
- MRR

Generation evaluation will include:

- answer relevance
- faithfulness
- citation correctness
- required fact coverage
- unsupported claims
- correct abstention

The project will also compare different approaches such as:

```text
Vector Search
      vs
Hybrid Search

No Reranker
      vs
Reranker

Different Chunking Strategies
```

The goal is to measure whether each improvement actually improves the system.

---

## Repository Structure

```text
opsrag/
├── README.md
├── docs/
│   ├── use-cases.md
│   └── architecture.md
├── knowledge-base/
│   ├── kafka/
│   ├── lambda/
│   └── eks/
├── datasets/
│   └── evaluation/
├── src/
│   └── opsrag/
├── tests/
├── infrastructure/
├── docker-compose.yml
└── pyproject.toml
```

The structure will evolve as the implementation progresses.

---

## What This Project Demonstrates

OpsRAG is primarily a portfolio project focused on practical AI Engineering skills:

- RAG architecture
- embeddings
- vector databases
- hybrid retrieval
- reranking
- structured outputs
- hallucination reduction
- RAG evaluation
- LLM observability
- AI security
- backend development
- AWS
- Infrastructure as Code

The objective is not to build another chatbot over documents.

The objective is to build a **measurable, traceable, and production-oriented RAG system for incident investigation**.