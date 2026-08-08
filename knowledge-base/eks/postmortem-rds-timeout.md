---
title: Historical RDS Timeout from EKS Backend
domain: eks
document_type: postmortem
environment: production
service: payments-api
status: historical
date: 2026-06-03
---

# Historical RDS Timeout from EKS Backend

## Summary

On 2026-05-27, `payments-api` pods in the production EKS cluster reported intermittent timeouts while connecting to their PostgreSQL RDS cluster. The issue lasted 22 minutes and affected payment status refresh jobs. Customer checkout traffic continued through cached status responses.

This was a different service and database than `orders-api`, but the incident remains useful because it describes how teams separated DNS, TCP connectivity, NetworkPolicy, Security Groups, and authentication during an RDS timeout.

## Detection

The first alert came from readiness probe failures. Application logs showed that DNS resolution succeeded and that connection attempts timed out on port 5432. The database was available in RDS inventory, and there were no corresponding PostgreSQL authentication failures in database logs.

## Investigation

The response team checked the configured endpoint and confirmed it matched the expected production database. They then ran TCP tests from a debug pod with the same labels as the application. A second debug pod with different labels had different connectivity behavior, which shifted attention to workload-level policy controls.

AWS security group rules were reviewed in parallel. The RDS security group allowed PostgreSQL from the expected EKS node security group and did not allow public access. Route tables and subnet NACLs showed no recent changes.

## Resolution and follow-up

The service owner updated the relevant policy and added a pre-deploy connectivity check for database migrations. Platform owners also added runbook language clarifying that a timeout is not the same as an authentication failure.

Historical incidents should not be copied onto current incidents without fresh evidence. For any new RDS timeout, collect the current namespace, pod labels, endpoint, DNS result, TCP result, NetworkPolicies, security groups, and RDS status.
