---
title: Order Events Publisher Architecture
domain: lambda
document_type: architecture
environment: production
service: order-events-publisher
status: current
date: 2026-07-10
---

# Order Events Publisher Architecture

`prod-order-events-publisher` is a Node.js 20 Lambda function that publishes order lifecycle events after reading transaction state from the orders database. The function is deployed in `us-east-1` and attached to the `prod` VPC (`vpc-0f1a2b3c4d5e6f70a`) using two private subnets:

- `subnet-0a11b22c33d44e501`
- `subnet-0a11b22c33d44e502`

The function has two expected dependencies:

```text
Lambda: prod-order-events-publisher
  |-- RDS PostgreSQL: prod-orders-db.cluster-c8example.us-east-1.rds.amazonaws.com:5432
  `-- SNS topic: arn:aws:sns:us-east-1:123456789012:prod-order-events
```

## RDS path

The RDS PostgreSQL cluster is private and resides in the same VPC. It is not publicly accessible. Lambda reaches it over private VPC routing on port 5432. The RDS security group allows traffic from the Lambda security group used by the function. This path does not require internet egress.

## SNS path

SNS is a regional AWS service reached through the `sns.us-east-1.amazonaws.com` HTTPS endpoint unless a service-specific VPC Interface Endpoint is present. A Lambda function in private subnets needs a route through NAT Gateway or a matching SNS VPC Endpoint to call SNS without public subnet placement.

The production VPC includes an S3 Gateway Endpoint for artifact and batch data access. That endpoint does not provide private connectivity to SNS. Security groups and IAM permissions still need to be checked, but they are separate from route availability to the SNS HTTPS endpoint.

## Operational note

When investigating failures, separate database connectivity from AWS API connectivity. A successful PostgreSQL connection confirms the Lambda has private VPC access to RDS; it does not confirm that the private subnets can reach every regional AWS API over port 443.
