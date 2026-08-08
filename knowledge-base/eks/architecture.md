---
title: Orders API EKS to RDS Architecture
domain: eks
document_type: architecture
environment: production
service: orders-api
status: current
date: 2026-07-13
---

# Orders API EKS to RDS Architecture

`orders-api` runs in the `prod` namespace on the production EKS cluster. The application stores order state in PostgreSQL on RDS. The configured database endpoint is:

```text
prod-orders-db.cluster-c8example.us-east-1.rds.amazonaws.com:5432
```

The expected request path is:

```text
orders-api pod
      |
EKS pod networking
      |
VPC routing and policy controls
      |
RDS PostgreSQL
```

## Runtime placement

The workload is deployed as a Kubernetes Deployment with the label `app.kubernetes.io/name=orders-api`. The pods use cluster DNS to resolve the RDS endpoint and connect to PostgreSQL on TCP port 5432.

NetworkPolicy enforcement is enabled for the production EKS cluster. Namespace-level policies are part of the standard control set for backend workloads. A policy that selects a pod can limit egress destinations even when the AWS VPC route table and RDS security group would otherwise allow traffic.

## Database placement

The RDS cluster identifier is `prod-orders-db`. It is private, not publicly accessible, and deployed in private subnets in `vpc-0f1a2b3c4d5e6f70a`. Platform inventory shows the RDS cluster status as `available`. The RDS security group is intended to allow PostgreSQL from the production EKS node security group on port 5432.

## Operational boundaries

Ingress traffic into `orders-api` is handled separately through the platform ALB and Kubernetes Ingress. That path is not used for pod-to-database connections. For database incidents, prioritize endpoint, DNS, TCP connectivity, NetworkPolicy, and AWS security controls before investigating HTTP ingress routing.
