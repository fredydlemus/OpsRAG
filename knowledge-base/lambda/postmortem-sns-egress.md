---
title: Historical Private Subnet AWS API Egress Incident
domain: lambda
document_type: postmortem
environment: production
service: async-notifications
status: historical
date: 2026-04-28
---

# Historical Private Subnet AWS API Egress Incident

## Summary

On 2026-04-21, the `async-notifications` service lost the ability to call a regional AWS API from private subnets after a network cleanup removed an unused NAT route table association. The affected workers could still reach Redis and RDS inside the VPC, which initially made the incident look like a service-specific SDK issue.

The incident is relevant as a diagnostic pattern: private connectivity to internal dependencies does not prove that a workload has outbound access to AWS APIs.

## Impact

Notification delivery was delayed for 37 minutes. The worker process retried publish operations until messages were moved to a dead-letter queue. No customer data was lost, but downstream alerts were delayed.

## Detection

Application logs showed repeated TCP timeouts to an AWS regional HTTPS endpoint. There were no `AccessDenied` responses and no change in IAM policy. Database health checks continued to pass. VPC Flow Logs showed attempted connections from private subnet addresses without completed return traffic.

## Resolution

The network team restored the intended egress path and added a validation check for regional API reachability from private subnets. The service team reduced retry fan-out to avoid thread exhaustion during future egress failures.

## Lessons

For Lambda functions or workers placed in private subnets, review routing and service endpoints before changing IAM when the symptom is a TCP timeout. A NAT Gateway and a VPC Endpoint solve different problems. Gateway endpoints such as S3 do not cover interface endpoint services, and interface endpoints are scoped to a specific AWS service and region.

This postmortem does not identify the cause of later SNS incidents by itself. It should be correlated with the current route tables, VPC endpoints, security group egress, IAM permissions, and logs.
