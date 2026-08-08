---
title: EKS Ingress Troubleshooting Guide
domain: eks
document_type: runbook
environment: production
service: platform-ingress
status: current
date: 2026-06-20
---

# EKS Ingress Troubleshooting Guide

This guide covers HTTP and HTTPS traffic entering EKS through the platform Application Load Balancer. It is useful when users report 404, 502, 503, TLS certificate, host header, or path routing problems for public or internal APIs.

## Scope

Ingress troubleshooting starts at the load balancer and moves inward:

- Route 53 record and DNS target.
- ALB listener, certificate, and rule priority.
- Kubernetes Ingress object and annotations.
- Target group health.
- Service selector and endpoint readiness.
- Pod readiness and application HTTP logs.

This path is separate from backend egress to databases. A pod connecting to PostgreSQL on RDS does not use the ALB, Ingress object, or HTTP listener rules.

## Common symptoms

HTTP 404 usually indicates that the request reached a listener but did not match the expected host or path rule. HTTP 502 can indicate that the target closed the connection or returned an invalid response. HTTP 503 commonly appears when no healthy targets are available. TLS failures may be caused by an expired certificate, wrong SNI name, or listener policy mismatch.

## Evidence to collect

Collect the hostname, path, response code, ALB request ID, Ingress object, Service object, target group health, and recent deployment changes. For application-level 5xx responses, compare pod logs with ALB access logs.

## Out of scope

This document does not diagnose PostgreSQL connection timeouts, RDS security groups, Kubernetes NetworkPolicy egress, or database authentication. For pod-to-RDS issues, use the database connectivity runbook and collect DNS and TCP evidence from the workload namespace.
