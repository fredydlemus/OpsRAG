---
title: Lambda VPC Networking Runbook
domain: lambda
document_type: runbook
environment: production
service: order-events-publisher
status: current
date: 2026-07-12
---

# Lambda VPC Networking Runbook

Use this runbook when a Lambda function attached to a VPC has connectivity issues. A VPC-attached Lambda uses elastic network interfaces in the configured subnets. That placement can provide private access to databases, caches, and internal services, but it changes how the function reaches public internet endpoints and regional AWS service endpoints.

## Classify the destination

Start by identifying the destination type:

- Private resource inside the same VPC, such as RDS, ElastiCache, or an internal load balancer.
- Private resource in a peered VPC or through Transit Gateway.
- Regional AWS service endpoint, such as SNS, SQS, Secrets Manager, STS, or KMS.
- Public internet endpoint owned by a third party.

For private resources, verify subnet routing, security groups, NACLs, DNS resolution, and the destination listener. A database connection can work without a NAT Gateway when the database is reachable through private VPC routing.

For regional AWS services, check whether the service is reachable through a VPC Endpoint or through a NAT Gateway. Interface endpoints are service-specific. A VPC Endpoint for one service does not provide private access to all AWS APIs.

## NAT Gateway vs VPC Endpoint

A NAT Gateway allows workloads in private subnets to initiate outbound connections to public endpoints through an internet gateway. It is commonly used when functions need broad egress to AWS APIs or third-party services.

A VPC Endpoint provides private connectivity to a supported AWS service without requiring internet egress. Gateway endpoints are used for services such as S3 and DynamoDB. Interface endpoints are used for many regional APIs and create private IP addresses in selected subnets.

When a Lambda can reach RDS but times out calling an AWS API over HTTPS, do not treat the successful database connection as proof of general internet egress. RDS connectivity usually stays inside the VPC, while an API call to a regional service needs either a valid route to public AWS endpoints or a matching VPC Endpoint.

## Diagnostic order

Collect the function name, runtime, subnet IDs, security group, route tables, VPC endpoints, and the exact error. Distinguish TCP timeouts from authorization failures. IAM denial normally returns an explicit access denied response after reaching the service. A connection timeout before an HTTP response points first to routing, endpoints, DNS, security groups, or NACLs.

Confirm outbound security group rules, then inspect private subnet route tables. If there is no NAT route, confirm whether a service-specific endpoint exists for the failing AWS service.
