---
title: SNS Publish IAM Policy for Order Events Publisher
domain: lambda
document_type: reference
environment: production
service: order-events-publisher
status: current
date: 2026-07-11
---

# SNS Publish IAM Policy for Order Events Publisher

The Lambda execution role for `prod-order-events-publisher` includes permission to publish to the production order events topic. This document is used during incident review to distinguish authorization failures from network connectivity failures.

## Execution role

```text
role_name: prod-order-events-publisher-role
function: prod-order-events-publisher
region: us-east-1
topic: arn:aws:sns:us-east-1:123456789012:prod-order-events
```

## Inline policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublishOrderEvents",
      "Effect": "Allow",
      "Action": [
        "sns:Publish"
      ],
      "Resource": "arn:aws:sns:us-east-1:123456789012:prod-order-events"
    },
    {
      "Sid": "WriteFunctionLogs",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:us-east-1:123456789012:log-group:/aws/lambda/prod-order-events-publisher:*"
    }
  ]
}
```

## Diagnostic interpretation

An IAM denial for SNS normally appears as an AWS service response such as `AuthorizationError`, `AccessDenied`, or an HTTP 403 response from the SNS API. A TCP connection timeout to `sns.us-east-1.amazonaws.com:443` occurs earlier in the request path, before the service can evaluate this policy.

This policy should be checked when the SDK reaches SNS and receives an authorization response. It does not validate subnet routes, NAT Gateway availability, VPC Endpoint presence, DNS, or NACL behavior.
