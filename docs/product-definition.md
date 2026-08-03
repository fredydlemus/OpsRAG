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