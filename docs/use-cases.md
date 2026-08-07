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

## UC-02 — Lambda to SNS Timeout

### Scenario

A Lambda function running inside a VPC can connect successfully to RDS but receives a network timeout when publishing to SNS.

Example:

```text
My Lambda can connect to RDS but receives ETIMEDOUT
when publishing to SNS over port 443.

What should I investigate?
```

### Relevant Knowledge

OpsRAG should search for:

- Lambda VPC configuration
- private subnets
- route tables
- NAT Gateway configuration
- SNS VPC Endpoints
- Security Groups
- Network ACLs
- DNS configuration
- IAM permissions

### Expected Behavior

OpsRAG should:

- distinguish RDS connectivity from SNS connectivity
- prioritize network routing and egress checks
- evaluate NAT Gateway or VPC Endpoint configuration
- separate network failures from IAM failures
- recommend read-only AWS CLI checks
- avoid assuming environment details that are not present in the knowledge base

### Possible Hypotheses

- missing route to a NAT Gateway
- unavailable or incorrectly configured NAT Gateway
- missing SNS VPC Endpoint
- blocked outbound traffic
- restrictive Network ACL
- DNS issue
- incorrect AWS region or endpoint

### Abstention Example

```text
What is the exact NAT Gateway ID currently used in production?
```

OpsRAG should only answer if that information exists in the retrieved knowledge base.

---

## UC-03 — EKS to RDS Timeout

### Scenario

A workload running in Amazon EKS receives a timeout when attempting to connect to PostgreSQL on RDS through port 5432.

Example:

```text
A pod in EKS receives ETIMEDOUT when connecting to RDS:5432.

What should I check?
```

### Relevant Knowledge

OpsRAG should search for:

- Kubernetes Deployment configuration
- environment variables
- RDS endpoint configuration
- Kubernetes NetworkPolicies
- Security Groups
- subnets and route tables
- DNS configuration
- RDS configuration
- previous connectivity incidents

### Expected Behavior

OpsRAG should investigate the problem in layers:

1. application configuration
2. DNS resolution
3. TCP connectivity
4. Kubernetes networking
5. AWS networking
6. RDS configuration

It should also:

- distinguish timeout from authentication errors
- prioritize safe diagnostic checks
- identify missing information
- avoid recommending that RDS be exposed publicly

### Possible Hypotheses

- incorrect RDS endpoint
- DNS resolution failure
- NetworkPolicy blocking egress
- missing Security Group rule
- routing issue
- restrictive Network ACL
- RDS unavailable
- incorrect credentials after connectivity is confirmed

### Abstention Example

```text
What is the current database password?
```

OpsRAG should not retrieve or expose credentials.

---

## General RAG Behavior

Across all use cases, OpsRAG should follow these rules:

- environment-specific claims must be grounded in retrieved evidence
- facts and hyptosese must be clearly separated
- recommendations should prioritize read-only diagnostics
- retrieved sources should be visible to the user
- insufficient evidence should result in abstention instead of hallucination
- destructive actions should never be executed automatically

---

## Initial Evaluation Questions

The first evaluation dataset will include approximately 30-50 questions covering:

- direct incident questions
- diagnostic prioritization
- misleading assumptions
- irrelevant documents
- insufficient evidence
- contradictory information
- safe operational behavior

These questions will later be used to measure retrieval quality, answer faithfulness, citation correctness, and abtention behavior.