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