# OpsRAG — Product Definition

## 1. Summary

**OpsRAG** is a technical incident investigation assistant based on Retrieval-Augmented Generation, designed to help DevOps engineers, SREs,
Cloud Engineers, and Platform Engineers investigate problems in infrastructure, applications, and distributed services.

The system queries a knowledge base composed of runbooks, postmortens, configurations, Kubernetes manifests, Terraform code, logs, 
and architecture documentation.

Given a technical question, OpsRAG retrieves relevant evidence ang generates a structured diagnosis that includes:

- Problem summary.
- Hypotheses ranked by relevance.
- Evidence associated with each hypothesis.
- Recommended checks.
- Diagnostic commands.
- Risk level of the commands.
- Source used.
- Limitations and level of uncertainty.

OpsRAG must no be presented as a system that resolves incidents automatically. Its puropose is to help the engineer investigate faster,
in a more structured and verifiable way.

---

## 2. Problem
 
During a technical incident, engineers must consult information scattered across multiple sources:
 
- Runbooks.
- Wikis.
- Postmortems.
- Infrastructure repositories.
- Kubernetes manifests.
- Configurations.
- Logs.
- Dashboards.
- Vendor documentation.
- Historical conversations and tickets.

This information can be incomplete, duplicated, outdated, or expressed with different terminology.
 
This causes the investigation process to depend excessively on:
 
- The individual engineer's experience.
- The team's tribal knowledge.
- The ability to quickly find the right document.
- Manual interpretation of configurations and error messages.
- Memory of past incidents.

Traditional search engines can locate documents cotaninig specific words, but they don't always identify conceptually realted documents.
 
Language models can generate technical explanations, but without access to organization-specific information they can:
 
- Invent configurations.
- Recommend actions incompatible with the existing architecture.
- Ignore previous incidents.
- Confuse general best practices with facts about the environment.
- Present hypotheses as if they were verified conclusions.

OpsRAG aims to combine semantic search, textual retrieval, and LLM-based generation to produce diagnoses backed by evidence.
 
---

## 3. Target user
 
### Primary user
 
DevOps Engineer, SRE, Cloud Engineer, or Platform Engineer responsible for investigating incidents in development, testing, or production environments.
 
### Expected background knowledge
 
The user is familiar with concepts such as:
 
- AWS.
- Kubernetes.
- EKS.
- Terraform.
- Networking.
- Databases.
- Kafka.
- Observability.
- Logs and metrics.

OpsRAG does not replace this knowledge. It complements it through search, correlation, and organization of evidence.
 
### User needs
 
The user needs to:
 
- Quickly find documentation related to an incident.
- Compare the current problem with previous incidents.
- Get a ranked list of possible causes.
- Identify what to validate first.
- Know what evidence supports each hypothesis.
- Get safe diagnostic commands.
- Distinguish facts, inferences, and assumptions.
- Avoid manually reviewing dozens of documents.
---

## 4. Value proposition

OpsRAG reduces the time needed to start investigating an incident by transforming a technical question into a structured set of
hypotheses, checks, and evidence.

The value proposition can be summarized as:

> Help engineers investigate technical incidents using their own organization's operational knowledge, without losing traceability over sources and without presenting assumptions as facts.

---

## 5. MVP use cases

The MVP will focus on three scenarios.

### 5.1 Kafka with high CPU consumption

Example question:

> Broker `prod-kafka-0` is consistently using approximately 2.5 CPU. What could be the causes, and what should I check first?

Potential sources:

- Pod resource configuration.
- JMX Exporter configuration.
- Prometheus metrics.
- Kafka runbook.
- Postmortens of previous incidents.
- Consumer configuration.
- Partition configuration.
- Strimzi manifests.

Expected response:

- Identification that consumption is near the configured limit.
- Hyposteses about throttling, load, partitions, metrics, or gabage collection.
- retrieved evidence.
- Validation commands.
- Prioritization of checks.

### 5.2 Lambda inside a VPC without access to SNS
 
Example question:
 
> My Lambda connects successfully to RDS, but times out when publishing a message to SNS over port 443. What should I check?
 
Potential sources:
 
- Network diagram.
- Route tables.
- Subnet configuration.
- Security groups.
- Lambda Terraform code.
- Internal documentation on NAT Gateway.
- Documentation on VPC Endpoints.
- Connectivity runbook.

Expected response:
 
- Differentiation between connectivity to RDS and connectivity to public AWS services.
- Hypotheses related to NAT Gateway, routes, and VPC Endpoint.
- Specific checks.
- Environment evidence.
- Read-only AWS CLI commands or queries.

### 5.3 Application in EKS without connection to RDS
 
Example question:
 
> A pod in EKS gets a timeout connecting to PostgreSQL on port 5432. What components should I validate?
 
Potential sources:
 
- Security groups.
- Subnets.
- Network policies.
- Kubernetes Services.
- DNS configuration.
- RDS and EKS Terraform code.
- Environment variables.
- Connectivity runbooks.
- Related postmortems.

Expected response:
 
- Ranked list of possible causes.
- Validation from the application layer down to the network.
- Evidence associated with each recommendation.
- Safe Kubernetes and AWS commands.
- Separation between DNS, routing, firewall, and credentials issues.
---

## 6. MVP scope

The MVP will include the following capabilities.

### Document ingestion

The system will initially be able to process:

- Markdown.
- Plain text.
- JSON.
- YAML.
- Terraform.
- Text Logs.

### Retrieval

The system will use:

- Vector search.
- Textual search.
- Metadata filters.
- Hybrid retrieval.
- Result ranking.

### Generation

The system will produce:

- Structured responses.
- Hypotheses.
- Evidence.
- Recommendations.
- Diagnostic commands.
- Citations.
- Limitations.
- Uncertainty indicators.

### Evaluation

The system will have an initial set of evaluation questions with:

- Expected relevant documents.
- Facts that must appear.
- Claims that must not be generated.
- Cases where the system should abstain.

### Interface

The MVP will have an interface that allows the user to:

- Write a question.
- View the answer.
- View the retrieved resources.
- View the fragments used.
- View the retrieval scores.
- Consult the basic execution trace.

---

## 7. Out of scope for the MVP
 
The following features will not be part of the first version:
 
- Automatic execution of commands.
- Infrastructure modification.
- Automatic pod restarts.
- Direct access to production clusters.
- Real-time CloudWatch queries.
- Real-time Prometheus queries.
- PagerDuty integration.
- Slack integration.
- Autonomous agents.
- GraphRAG.
- Direct analysis of images or dashboards.
- Multimodal diagnostics.
- Automatic remediation.
- Automatic generation of Terraform changes.
- Automatic application of Kubernetes manifests.
- Multi-company or multi-tenant access.

These capabilities can be evaluated after validating the quality of conventional RAG.
 
---

## 8. Knowledge sources

The initial knowledge base will be composed of documents created specifically for the three MVP use cases.

### Document types

- Runbooks.
- Postmortems.
- ADRs.
- Architecture documentation.
- Terraform fragments.
- Kubernetes manifests.
- Kafka configurations.
- Observability configurations.
- Logs.
- Command outputs.
- Diagnostic procedures.
- Network documentation.

### Main metadata

Each document or fragment may include:

- Service.
- Environment.
- Document type.
- Creation date.
- Last updated date.
- Severity.
- Incident type.
- Source.
- Version.
- Region.
- Cluster.
- Namespace.
- Confidentially level.

---

## 9. System input

The main input will be a technical question written in natural language.

Example:

> The Kafka broker is constantly near its CPU limit, but consumers have no lag. What could be causing this?

The query may contain:

- Service name.
- Resource name.
- Environment.
- Error message.
- Port.
- Observed metric.
- Command output.
- Symptom.
- Recent change.

The MVP will not require the user to fill in all these fields in a structured way.

---

## 10. System output

The response must be structured and validated against schema.

Conceptual example:

```json
{
  "summary": "The broker is operating near its configured CPU limit.",
  "severity": "high",
  "confidence": 0.82,
  "hypotheses": [
    {
      "cause": "Overload generated by JMX metrics exposure",
      "confidence": 0.78,
      "reasoning": "The endpoint exposes a large number of series and each request takes several seconds.",
      "evidence": [
        {
          "source_id": "chunk-001",
          "source": "kafka/metrics/jmx-analysis.md",
          "statement": "The endpoint exposes more than 33,000 lines of metrics."
        }
      ]
    }
  ],
  "recommended_checks": [
    {
      "priority": 1,
      "description": "Check whether the container is being CPU throttled.",
      "command": "kubectl top pod ...",
      "risk": "read-only",
      "expected_result": "Confirm whether usage remains near the limit."
    }
  ],
  "limitations": [
    "No CPU profile of the Java process is available."
  ],
  "sources": [
    {
      "source_id": "chunk-001",
      "document": "kafka/metrics/jmx-analysis.md"
    }
  ]
}
```

---