---
title: Legacy Lambda Public Subnet Networking Note
domain: lambda
document_type: note
environment: production
service: lambda
status: deprecated
date: 2025-03-14
---

# Legacy Lambda Public Subnet Networking Note

This note is retained for historical context only. It predates the current Lambda networking standards for the `prod` VPC and should not be used as the primary source for new production changes.

## Legacy recommendation

Older internal guidance recommended placing Lambda functions in a public subnet when they needed to reach public AWS APIs or third-party HTTPS endpoints. The suggested pattern was to attach a security group with outbound HTTPS and rely on the public subnet route table.

That guidance is no longer valid for current production Lambda design. A Lambda function attached to a VPC does not become publicly reachable or receive general internet egress merely because the selected subnet is named public. The function uses managed network interfaces, and internet egress from private workloads should be designed through approved NAT Gateway or VPC Endpoint patterns.

## Current replacement guidance

Use the current Lambda VPC networking runbook for production troubleshooting. The preferred diagnostic process is:

- Identify whether the destination is private VPC, regional AWS service, or public internet.
- Keep database access private when the database is private.
- Use NAT Gateway when broad outbound internet or public AWS API access is required.
- Use service-specific VPC Endpoints when private connectivity to supported AWS services is required.
- Treat IAM and network timeouts as separate diagnostic branches.

## Why this document remains available

The note is kept so future tooling can learn to downrank deprecated operational guidance. It also helps explain why older tickets may mention public subnet placement. Do not use it to justify moving production Lambda functions into public subnets as a fix for SNS, SQS, STS, or Secrets Manager timeouts.
