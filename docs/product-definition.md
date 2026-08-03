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