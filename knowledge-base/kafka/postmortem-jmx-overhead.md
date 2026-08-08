---
title: Historical Kafka Metrics Exporter Overhead
domain: kafka
document_type: postmortem
environment: production
service: kafka
status: historical
date: 2026-05-09
---

# Historical Kafka Metrics Exporter Overhead

## Summary

On 2026-05-02, the `analytics-prod` Kafka cluster experienced elevated CPU on two brokers after a metrics configuration change. The incident affected dashboards and alert quality but did not cause message loss. Producers continued to publish and most consumer groups remained close to real time.

This note is retained because it describes an operational pattern that can reappear in Kafka environments: observability configuration can create measurable broker work. It should be used as background evidence, not as proof for unrelated incidents.

## What happened

A new JMX exporter rule set was deployed to improve topic-level visibility. The configuration matched per-topic, per-partition, and per-client metrics for producers and consumers. The affected cluster had a high partition count and many short-lived clients, which increased the number of generated time series. Prometheus was scraping the metrics endpoint every 30 seconds.

During the incident window, the `/metrics` endpoint response time increased from less than 5 seconds to over 18 seconds on the busiest brokers. CPU usage rose at the same time, and dashboards showed additional pressure from request handling and garbage collection. Consumer lag did not identify the issue because the cluster was still able to serve consumers within the normal delay budget.

## Response

The response team compared broker CPU, scrape duration, metric count, request rates, and GC pause time. After confirming that client traffic had not increased enough to explain the change, they reduced the broadest JMX rules and added metric relabeling for unused labels. CPU returned to normal after the updated exporter configuration rolled out.

## Follow-up guidance

When investigating Kafka CPU, check exporter behavior together with broker workload. Useful signals include exported time series count, scrape duration, Prometheus target health, CPU throttling, leader partition distribution, and request rate by API key.

Do not assume that a past metrics incident explains a current CPU alert. Validate current cluster limits, traffic, partition placement, JVM behavior, and replication state before narrowing the hypothesis.
