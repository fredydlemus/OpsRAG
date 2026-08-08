---
title: EKS to RDS Database Connectivity Runbook
domain: eks
document_type: runbook
environment: production
service: orders-api
status: current
date: 2026-07-16
---

# EKS to RDS Database Connectivity Runbook

Use this runbook when a pod running in EKS cannot connect to PostgreSQL on RDS. The expected production pattern is pod to cluster networking, then VPC routing, then RDS listener on port 5432. A timeout should be investigated as a network path problem before treating it as a database password or application credential problem.

## Diagnostic order

1. Review the exact application error.
2. Confirm the configured endpoint and port.
3. Verify DNS resolution from the pod or an equivalent debug pod.
4. Test TCP connectivity to the resolved address and port.
5. Review NetworkPolicy selection and egress rules.
6. Review Security Groups for Pods, node security groups, and RDS security groups.
7. Review route tables and NACLs for the involved subnets.
8. Confirm RDS status, listener, and maintenance events.
9. Check database authentication only after TCP connectivity is established.

## Error interpretation

`connect ETIMEDOUT <ip>:5432` indicates that the client did not complete a TCP connection to the database listener. This is different from password authentication failed, no pg_hba.conf entry, database does not exist, or TLS negotiation failure. Authentication problems require the TCP connection to reach PostgreSQL far enough for the server to respond.

If DNS resolution succeeds and the endpoint is correct, focus on packet flow and policy enforcement. EKS clusters may enforce Kubernetes NetworkPolicies through the configured CNI policy engine. A policy that selects the application pods and defines egress can limit destinations even when AWS security groups are correct.

## Evidence to collect

Capture the namespace, deployment name, pod labels, configured database host, database port, DNS lookup result, TCP test result, NetworkPolicies in the namespace, RDS security group rules, and RDS status. Include timestamps and pod names. Do not collect database passwords or Secret values; references to Kubernetes Secret names are sufficient.

## Common branches

If DNS fails, inspect CoreDNS, cluster DNS policy, and VPC resolver behavior. If DNS succeeds but TCP times out, inspect NetworkPolicy, security groups, NACLs, and routes. If TCP connects but authentication fails, then inspect username, password source, TLS mode, and database-level grants.
