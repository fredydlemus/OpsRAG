# Use Cases

OpsRAG will initially focus on three operational incident scenarios.

The objective of these use cases is to define what the system should investigate, what knowledge it should retrieve, and how it should behave evidence is insufficient.

---

## UC-01 - Kafka High CPU

### Scenario

A Kafka broker is consistenly running close its configured CPU limit, while consumer lag remains at zero.

Example:

```text
prod-kafka-0 is constantly using around 2.5 CPU.
Consumer lag is zero.

What should I investigate?
```

### Relevant Knowledge

OpsRAG should search for information related to:

- Kafka CPU limits
- CPU throttling
- JMX Exporter configuration
- Prometheus scraping
- partition distribution
- producer/request load
- JVM garbage collection
- previous Kafka incidents

### Expected Behavior

OpsRAG should:

- detect that CPU usage is close to the configured limit
- propose multiple possible causes
- explain that zero consumer lag does not mean low broker load
- prioritize diagnostic checks
- provide supporting evidence
- recommend read-only commands
- avoid claiming a root cause without enough evidence

### Possible Hypotheses

- CPU throttling
- JMX metrics overhead
- excessive Prometheus scraping
- high partition count
- producer or request load
- garbage collection
- replication activity

### Abstention Example

```text
Which Java thread consumed the most CPU yesterday at 14:35?
```

OpsRAG should indicate that there is not enough evidence unless a CPU profile, JFR, threath dump, or equivalent diagnostic data exists.

---