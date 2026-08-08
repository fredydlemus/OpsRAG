---
title: Kafka High CPU Runbook
domain: kafka
document_type: runbook
environment: production
service: kafka
status: current
date: 2026-07-15
---

# Kafka High CPU Runbook

This runbook is used when one or more Kafka brokers show sustained CPU usage above normal operating range. The goal is to collect enough evidence to separate broker saturation, client traffic, JVM pressure, replication work, and observability overhead. Do not start by assuming that consumer lag explains the CPU level. A broker can process high producer traffic, replication traffic, controller work, or metrics collection while consumer lag remains low.

## Initial checks

Identify the affected broker, namespace, and time window. Compare current CPU usage with the configured request and limit for the Kafka container. If the observed usage is near the limit, check whether the container reports throttling. CPU throttling may appear as higher request latency, delayed network threads, or unstable scrape duration even when the process remains healthy.

Collect:

- CPU usage and throttling metrics for the broker container.
- Kafka network processor idle percentage.
- Request rate by API key, especially Produce, Fetch, Metadata, and OffsetCommit.
- Bytes in/out per second and request queue size.
- JVM garbage collection frequency and pause time.
- Partition count and leader partition distribution per broker.
- Under-replicated partitions, ISR changes, and replication fetcher activity.

## Client and traffic review

Check whether load is producer-heavy, consumer-heavy, or metadata-heavy. Consumer lag is useful, but lag alone does not measure total broker work. Producer request rate, compression cost, acknowledgements, and replication fan-out can keep CPU high while consumers are caught up.

Review recent deploys for services that increased producer batch rate, reduced linger time, changed compression, or added topic partitions. Also compare leader partition balance across brokers. A broker with more leaders for hot topics may show higher CPU than peers without visible consumer lag.

## JVM and metrics review

Inspect JVM GC metrics before changing heap settings. Short and frequent pauses may indicate allocation pressure, while long pauses may indicate heap pressure. Compare heap usage, old generation occupancy, and GC pause quantiles against the incident window.

Review the metrics exporter and Prometheus scrape behavior. A broad JMX exporter configuration can expose a large number of time series. Scrape duration, endpoint response time, and the number of exported metrics should be checked alongside CPU usage. Treat this as one hypothesis among several; correlate it with traffic, throttling, and JVM evidence before assigning cause.

## Escalation notes

If CPU remains near limit with throttling, capture current broker config, scrape config, JMX exporter config, consumer group lag, and a metrics snapshot. Avoid restarting brokers until replication health and ISR status have been reviewed.
