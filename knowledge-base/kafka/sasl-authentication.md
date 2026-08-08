---
title: Kafka SASL Authentication Operations
domain: kafka
document_type: reference
environment: production
service: kafka
status: current
date: 2026-06-18
---

# Kafka SASL Authentication Operations

The production Kafka clusters use SASL/SCRAM for application authentication on the internal TLS listener. This document describes routine operational checks for authentication failures, credential rotation, and client onboarding. It is primarily useful when producers or consumers receive authorization or authentication errors.

## Listener and user model

Applications connect through the internal bootstrap service for the cluster namespace. Each application owns a KafkaUser resource managed by Strimzi. User names should match the owning service name and environment. Shared credentials across services are not permitted.

The platform team rotates SCRAM credentials during scheduled maintenance windows. Application teams must consume credentials from Kubernetes Secrets mounted into their workloads or exposed through approved environment variables. Credentials must not be copied into Helm values, Terraform variables, runbooks, or incident notes.

## Common symptoms

Authentication incidents usually produce explicit log entries. Examples include failed SASL handshake, invalid credentials, unknown user, or connection closed during authentication. These errors differ from broker-side CPU saturation or client-side timeout symptoms. A successful authentication does not guarantee that the client has ACLs for every topic.

Check the following when authentication errors are reported:

- KafkaUser exists in the same namespace as the application owner.
- Secret name matches the deployment reference.
- Client properties include `security.protocol=SASL_SSL`.
- SCRAM mechanism is configured consistently.
- ACLs include the required topic and consumer group resources.
- The client truststore or platform CA bundle is current.

## Rotation procedure

Before rotation, notify service owners and confirm that deployments read credentials dynamically or can be restarted. Rotate one service at a time when possible. After rotation, confirm that produce and consume operations succeed for the service and that no authentication failure alerts remain.

Never paste real passwords, SCRAM material, tokens, or private keys into tickets or chat transcripts. Use redacted placeholders when collecting diagnostic context.
