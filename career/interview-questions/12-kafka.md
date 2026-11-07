# 12. Kafka — topics, partitions, consumer groups, exactly-once

Kafka comes up in almost every backend system-design round ("put a queue here — which one and why?"). A 3-year
engineer must explain partitions, consumer groups, offsets and delivery guarantees without notes, and know when
**not** to use Kafka. Syllabus: 2D Kafka (`../../syllabus.html`).

## 12.1 Why Kafka — the log, and Kafka vs other queues
**Learn:** DDIA ch11 "Partitioned logs" (pdf p449–454) · *Kafka: The Definitive Guide* ch.1 · Kreps, "The Log: What every software engineer should know about real-time data" (engineering.linkedin.com) · https://developer.confluent.io/courses/apache-kafka/events/
- [ ] `L1` What is Kafka, in one sentence?
- [ ] `L1` What is an event / record / message in Kafka? What fields does a record have? ↳ key, value, headers, timestamp, offset
- [ ] `L1` What is a topic? What is a partition? What is an offset?
- [ ] `L1` What is a broker? What is a cluster?
- [ ] `L1` What is a producer and what is a consumer?
- [ ] `L1` Why is Kafka called a "distributed commit log"?
- [ ] `L2` Message queue vs log: what is the difference in how messages are consumed and deleted? ↳ queue deletes on ack; log keeps, consumers track position
- [ ] `L2` Kafka vs RabbitMQ: when would you pick each? ↳ replay, throughput, ordering per partition vs routing, per-message ack, priorities
- [ ] `L2` Kafka vs Redis Streams: when is Redis Streams enough?
- [ ] `L2` Kafka vs AWS SQS / SNS / Kinesis / Google Pub/Sub / Azure Service Bus / Event Hubs.
- [ ] `L2` Kafka vs a database table used as a queue (`SELECT … FOR UPDATE SKIP LOCKED`).
- [ ] `L2` Why is Kafka fast even though it writes to disk? ↳ sequential append, page cache, batching, zero-copy sendfile, compression
- [ ] `L2` Why can many consumers read the same data in Kafka without slowing each other down?
- [ ] `L2` What does "replay" mean, and give a real case where you need it.
- [ ] `L2` What are typical use cases for Kafka? Give three you have seen.
- [ ] `L2` When should you **not** use Kafka? ↳ low volume, request/reply, per-message routing/priority, tiny team, delays/scheduling
- [ ] `L3` What is the "log as the source of truth" idea, and how does it relate to event sourcing and CDC?
- [ ] `L3` Why does Kafka push ordering and position tracking onto the consumer instead of the broker?
- [ ] `L3` Your team wants Kafka for 50 events per minute. What do you say?

## 12.2 Topics, partitions and keys
**Learn:** *Kafka: The Definitive Guide* ch.3 "Partitions" · DDIA ch6 "Partitioning" (pdf p209–231) · https://kafka.apache.org/documentation/#intro_concepts_and_terms
- [ ] `L1` Why does a topic have partitions?
- [ ] `L1` Where is ordering guaranteed in Kafka? ↳ only within a partition
- [ ] `L1` How does a producer decide which partition a record goes to? ↳ explicit partition, hash(key) mod N, sticky partitioner when no key
- [ ] `L2` What key would you choose for an orders topic? For a chat-messages topic? For a clickstream topic?
- [ ] `L2` What happens to ordering if you send records with no key?
- [ ] `L2` What is a hot partition? How do you detect it and fix it? ↳ skewed key; per-partition lag/bytes; salt key, split entity, more partitions
- [ ] `L2` How many partitions should a topic have? How do you decide? ↳ target throughput ÷ per-partition throughput; max consumers; future growth
- [ ] `L2` Can you increase the partition count of an existing topic? What breaks? ↳ key→partition mapping changes; ordering per key breaks
- [ ] `L2` Can you decrease the partition count? What do you do instead?
- [ ] `L2` What does a partition look like on disk? ↳ segment files, .log + .index + .timeindex, active segment
- [ ] `L3` What are the costs of too many partitions? ↳ open files, metadata, leader elections, rebalance time, end-to-end latency
- [ ] `L3` Explain the sticky partitioner and why it replaced round-robin for keyless records.
- [ ] `L3` You need global ordering across all events. What are your options and what do they cost?
- [ ] `L3` How would you write a custom partitioner, and when would you need one?

## 12.3 Producers — acks, batching, retries, idempotence
**Learn:** *Kafka: The Definitive Guide* ch.3 "Kafka Producers" + ch.8 "Exactly-Once Semantics" · https://kafka.apache.org/documentation/#producerconfigs
- [ ] `L1` What do `acks=0`, `acks=1` and `acks=all` mean?
- [ ] `L1` Which `acks` setting can lose data, and when?
- [ ] `L2` What do `linger.ms` and `batch.size` do? How do they trade latency for throughput?
- [ ] `L2` Which compression types does Kafka support, and where does compression happen? ↳ gzip/snappy/lz4/zstd; per batch at producer
- [ ] `L2` What happens when the producer's buffer is full? ↳ `buffer.memory`, `max.block.ms`, send blocks then throws
- [ ] `L2` Producer retries can create duplicates. Why? ↳ ack lost after broker wrote; producer resends
- [ ] `L2` What is an idempotent producer? How does it work? ↳ producer id + per-partition sequence numbers; broker drops duplicates
- [ ] `L2` Why can retries reorder messages, and what does `max.in.flight.requests.per.connection` have to do with it?
- [ ] `L2` What is `delivery.timeout.ms` and how does it relate to `retries`?
- [ ] `L2` Synchronous vs asynchronous send with a callback: when do you use each?
- [ ] `L2` How do you handle a failed send in the callback? Retry, log, dead-letter, or crash?
- [ ] `L3` Walk me through everything that happens from `producer.send()` to the record being committed.
- [ ] `L3` You must not lose payment events even if a broker dies. List every producer and broker setting you set. ↳ acks=all, idempotence, min.insync.replicas=2, RF=3, no unclean election
- [ ] `L3` The database write succeeded but the Kafka send failed. Now what? ↳ dual-write problem → transactional outbox / CDC

## 12.4 Consumers, consumer groups and rebalancing
**Learn:** *Kafka: The Definitive Guide* ch.4 "Kafka Consumers" · https://developer.confluent.io/courses/architecture/consumer-group-protocol/
- [ ] `L1` What is a consumer group?
- [ ] `L1` How are partitions shared among consumers in one group?
- [ ] `L1` What happens if a group has more consumers than partitions?
- [ ] `L1` Two different groups read the same topic. Do they affect each other?
- [ ] `L2` How do you get "queue" behaviour and how do you get "pub/sub" behaviour with Kafka?
- [ ] `L2` What is a rebalance? What triggers one?
- [ ] `L2` What is "stop the world" rebalancing and why is it painful?
- [ ] `L2` Eager vs cooperative (incremental) rebalancing.
- [ ] `L2` What are static group membership and `group.instance.id` for? ↳ restart without rebalance during rolling deploys
- [ ] `L2` What do `session.timeout.ms`, `heartbeat.interval.ms` and `max.poll.interval.ms` control?
- [ ] `L2` A consumer takes 10 minutes to process one batch and keeps getting kicked out of the group. Why, and how do you fix it? ↳ max.poll.interval.ms; smaller max.poll.records; hand work to a pool, pause partitions
- [ ] `L2` What do `max.poll.records` and `fetch.min.bytes` / `fetch.max.wait.ms` do?
- [ ] `L2` What are the partition assignment strategies (range, round-robin, sticky, cooperative-sticky)?
- [ ] `L2` What is the group coordinator?
- [ ] `L2` Is a Kafka consumer thread-safe? How do you process in parallel inside one consumer?
- [ ] `L3` How do you scale consumption beyond the number of partitions? ↳ more partitions, or parallel per-key processing inside the consumer
- [ ] `L3` How do you keep per-key order while processing a partition with a thread pool?
- [ ] `L3` What happens to in-flight work when a partition is revoked during a rebalance? How do you avoid double processing? ↳ commit in onPartitionsRevoked
- [ ] `L3` Explain the newer consumer group protocol (KIP-848) and what it fixes.

## 12.5 Offsets and commits
**Learn:** *Kafka: The Definitive Guide* ch.4 "Commits and Offsets" · DDIA ch11 "Consumer offsets" (pdf p452)
- [ ] `L1` Where are consumer offsets stored? ↳ internal `__consumer_offsets` topic
- [ ] `L1` What does committing an offset mean?
- [ ] `L2` Auto-commit vs manual commit: what can go wrong with auto-commit?
- [ ] `L2` Commit before processing vs after processing: which guarantee does each give? ↳ before = at-most-once; after = at-least-once
- [ ] `L2` `commitSync` vs `commitAsync`: trade-offs and the usual combination.
- [ ] `L2` What does `auto.offset.reset` = `earliest` / `latest` / `none` do, and when does it apply?
- [ ] `L2` How do you reprocess a topic from yesterday 10:00? ↳ offsetsForTimes / kafka-consumer-groups --reset-offsets --to-datetime
- [ ] `L2` What happens when a committed offset points to data that retention already deleted?
- [ ] `L3` Can you store offsets outside Kafka (e.g. in Postgres with the results)? Why would you?
- [ ] `L3` What is the committed offset exactly — the last processed record or the next one to read?

## 12.6 Delivery guarantees — at-most-once, at-least-once, exactly-once
**Learn:** *Kafka: The Definitive Guide* ch.7 "Reliable Data Delivery" + ch.8 "Exactly-Once Semantics" · DDIA ch11 "Fault tolerance" (pdf p482–484) · https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/
- [ ] `L1` Define at-most-once, at-least-once and exactly-once.
- [ ] `L1` Which one is Kafka's default in practice?
- [ ] `L2` Is exactly-once delivery possible in a distributed system? What does Kafka actually promise? ↳ exactly-once *processing* within Kafka (read-process-write)
- [ ] `L2` What is an idempotent consumer? Give two ways to build one. ↳ dedupe table keyed by event id; upsert / natural idempotent writes
- [ ] `L2` How do Kafka transactions work? ↳ transactional.id, producer fencing, transaction coordinator, commit markers
- [ ] `L2` What is `isolation.level=read_committed`?
- [ ] `L2` What does `sendOffsetsToTransaction` do and why is it the key to read-process-write exactly-once?
- [ ] `L2` Kafka EOS ends at the Kafka boundary. You write to Postgres and call an email API. How do you get "effectively once"?
- [ ] `L3` What is a zombie producer and how does fencing with epochs stop it?
- [ ] `L3` What is the transactional outbox pattern? Draw it. ↳ write row + outbox in one DB txn; relay/CDC publishes
- [ ] `L3` Outbox relay crashes after publishing but before marking the row sent. What happens downstream?
- [ ] `L3` Where did you need at-most-once vs at-least-once in your own work? ↳ AiRA reminders: at-most-once with Redis locks — why that choice
- [ ] `L3` What is the performance cost of transactions and idempotence?

## 12.7 Replication, durability and the controller
**Learn:** *Kafka: The Definitive Guide* ch.6 "Kafka Internals" + ch.7 · DDIA ch5 "Leaders and Followers" (pdf p166–176) · https://kafka.apache.org/documentation/#replication
- [ ] `L1` What is the replication factor?
- [ ] `L1` What is a partition leader? What is a follower?
- [ ] `L1` Do consumers read from followers?
- [ ] `L2` What is the ISR (in-sync replica set)? When does a replica fall out of it?
- [ ] `L2` What does `min.insync.replicas` do, and how does it combine with `acks=all`?
- [ ] `L2` RF=3, `min.insync.replicas=2`, `acks=all`, two brokers die. What happens to producers? To consumers?
- [ ] `L2` What is the high watermark? Why can't consumers read past it?
- [ ] `L2` What is unclean leader election, and why is it off by default?
- [ ] `L2` What happens step by step when a leader broker crashes?
- [ ] `L2` What is the controller? What does it do?
- [ ] `L2` ZooKeeper vs KRaft: what changed and why?
- [ ] `L3` What is the leader epoch and what bug did it fix compared to the high-watermark-only design?
- [ ] `L3` What is rack awareness and why does it matter in a cloud with availability zones?
- [ ] `L3` Can Kafka lose acknowledged data? Name the exact settings under which it can. ↳ acks=1 + leader crash; unclean election; min.isr=1; fsync assumptions
- [ ] `L3` Kafka does not fsync every write by default. Why is it still durable enough?
- [ ] `L3` Follower fetching (KIP-392): when would you let consumers read from a follower?

## 12.8 Retention, compaction and storage
**Learn:** *Kafka: The Definitive Guide* ch.6 "Physical Storage" · DDIA ch11 "Log compaction" (pdf p459–460) · https://kafka.apache.org/documentation/#compaction
- [ ] `L1` How long does Kafka keep data? What controls it? ↳ retention.ms, retention.bytes, per topic
- [ ] `L1` What is log compaction?
- [ ] `L2` Delete vs compact cleanup policy: when do you use each? Can you use both?
- [ ] `L2` What is a tombstone? How do you delete a key from a compacted topic?
- [ ] `L2` Give a real use of a compacted topic. ↳ latest state per key: user settings, CDC table snapshot, `__consumer_offsets`
- [ ] `L2` What is a segment and why does retention delete whole segments, not single records?
- [ ] `L2` What is the maximum message size, and what do you do with a 50 MB payload? ↳ ~1 MB default; claim-check pattern (store in blob, send pointer)
- [ ] `L3` What is tiered storage and what problem does it solve?
- [ ] `L3` How do you handle a GDPR "delete my data" request when events are kept forever? ↳ compaction + tombstones, crypto-shredding
- [ ] `L3` How does the page cache + zero-copy path work on a consumer read?

## 12.9 Schemas, serialization and event design
**Learn:** DDIA ch4 "Formats for Encoding Data" (pdf p130–146) · *Kafka: The Definitive Guide* ch.3 "Serializers" · https://docs.confluent.io/platform/current/schema-registry/index.html
- [ ] `L1` Which serialization formats are common with Kafka? ↳ JSON, Avro, Protobuf
- [ ] `L2` What is a schema registry and why use one?
- [ ] `L2` Backward vs forward vs full compatibility: define each and give an example change.
- [ ] `L2` You need to add a required field to an event read by 6 services. How do you roll it out?
- [ ] `L2` Event notification vs event-carried state transfer: what goes in the payload?
- [ ] `L2` Fat events vs thin events: trade-offs.
- [ ] `L2` What should every event have? ↳ event id, type, version, timestamp, source, correlation id
- [ ] `L3` How do you version event types without breaking old consumers?
- [ ] `L3` One topic per event type, or one topic per entity with many types? Trade-offs for ordering.

## 12.10 Errors, retries and dead-letter topics
**Learn:** https://www.confluent.io/blog/error-handling-patterns-in-kafka/ · https://www.uber.com/blog/reliable-reprocessing/ (Uber retry topics)
- [ ] `L1` What is a dead-letter topic (DLT / DLQ)?
- [ ] `L2` A message cannot be parsed (poison pill). What does your consumer do?
- [ ] `L2` A downstream API is down for 10 minutes. Do you retry in place, pause, or move on? Why?
- [ ] `L2` How does a retry-topic chain work (retry-5s, retry-1m, DLT)? What does it do to ordering?
- [ ] `L2` How do you replay messages from a DLT after fixing the bug?
- [ ] `L3` Retrying in place blocks the partition; moving to a retry topic breaks per-key order. How do you choose per use case?
- [ ] `L3` How do you pause and resume consumption of a partition while a dependency recovers? ↳ consumer.pause/resume, keep polling for heartbeats

## 12.11 Operating Kafka — lag, monitoring, sizing
**Learn:** *Kafka: The Definitive Guide* ch.10–13 (administration, monitoring) · https://docs.confluent.io/platform/current/kafka/monitoring.html
- [ ] `L1` What is consumer lag?
- [ ] `L2` Consumer lag is growing. Walk me through how you debug it. ↳ slow processing vs too few consumers vs hot partition vs rebalance storms
- [ ] `L2` Which metrics would you put on a Kafka dashboard? ↳ lag, under-replicated partitions, ISR shrinks, request latency, bytes in/out, offline partitions
- [ ] `L2` What does "under-replicated partitions" mean and why page someone for it?
- [ ] `L2` How do you size a cluster for 100k messages/second of 1 KB each with 7 days retention and RF=3? ↳ ~100 MB/s in, ×3 replication, ~180 TB disk
- [ ] `L2` How do you do a rolling restart / upgrade of brokers without downtime?
- [ ] `L2` Managed Kafka (Confluent Cloud, MSK, Event Hubs Kafka API) vs self-hosted: trade-offs.
- [ ] `L3` How do you rebalance partitions across brokers after adding a broker? What does it cost?
- [ ] `L3` What are quotas and why does a multi-tenant cluster need them?
- [ ] `L3` How would you mirror a topic to another region (MirrorMaker 2 / cluster linking) and what happens to offsets?

## 12.12 Stream processing and the ecosystem
**Learn:** DDIA ch11 "Processing Streams" (pdf p464–484) · *Kafka Streams in Action* · https://kafka.apache.org/documentation/streams/
- [ ] `L1` What is Kafka Connect? Source vs sink connector.
- [ ] `L1` What is Debezium / CDC?
- [ ] `L2` What is Kafka Streams and how is it different from a plain consumer?
- [ ] `L2` KStream vs KTable.
- [ ] `L2` What is a windowed aggregation? Tumbling vs hopping vs sliding vs session windows.
- [ ] `L2` Event time vs processing time. What are late events and how are they handled?
- [ ] `L2` Stream–table join: give a use case.
- [ ] `L3` Where does Kafka Streams keep state, and how is it recovered after a crash? ↳ RocksDB local store + changelog topic
- [ ] `L3` Kafka Streams vs Flink vs Spark Structured Streaming: when each?
- [ ] `L3` How would you compute "top 10 trending products in the last 5 minutes" over a click topic?

## 12.13 Kafka in system design and in your work
**Learn:** HelloInt "Kafka deep dive" (hellointerview.com/learn/system-design/deep-dives/kafka) · DDIA ch12 "Unbundling databases"
- [ ] `L2` Design: an order service publishes `OrderPlaced`; inventory, email and analytics react. Draw topics, keys, groups.
- [ ] `L2` How would you use Kafka to decouple a slow LLM call from an HTTP request?
- [ ] `L2` How would you build a notification system on Kafka with per-user ordering and retries?
- [ ] `L2` Why might a startup choose Redis Streams or Postgres over Kafka? (Tie to AiRA: SSE → Redis Streams → WebSocket.)
- [ ] `L3` Design a saga for checkout (order → payment → inventory) with Kafka, including compensations.
- [ ] `L3` Design an audit log that must never lose an event and must be queryable for 7 years.
- [ ] `L3` You run 3 consumer groups (search indexer, analytics, email) on one topic. The email consumer is slow. Does it slow the others?
- [ ] `L3` Benchmark plan: Kafka vs Redis Streams for 10k msgs/s — what would you measure and what do you expect?

## 12.14 Rapid-fire round
- [ ] `L1` Ordering is guaranteed per ___? ↳ partition
- [ ] `L1` Default port of a Kafka broker?
- [ ] `L1` Who tracks the read position, the broker or the consumer?
- [ ] `L1` Does reading a message delete it?
- [ ] `L1` Max useful consumers in one group for a topic with 6 partitions?
- [ ] `L1` What is `__consumer_offsets`?
- [ ] `L1` What is a tombstone?
- [ ] `L1` What does `acks=all` wait for?
- [ ] `L1` What does ISR stand for?
- [ ] `L1` What replaced ZooKeeper?
- [ ] `L1` Name the four compression codecs.
- [ ] `L1` Which command shows the lag of a consumer group? ↳ kafka-consumer-groups --describe --group <name>
- [ ] `L1` What is a DLQ?
- [ ] `L1` What is CDC?
- [ ] `L1` Push or pull: how do Kafka consumers get data?
- [ ] `L1` What is a segment?
- [ ] `L1` Can two consumers in the same group read the same partition at the same time?
- [ ] `L1` What happens to a keyed record if you add partitions?
- [ ] `L1` What is an idempotent producer?
- [ ] `L1` What does `read_committed` hide from consumers?
- [ ] `L1` What is a rebalance?
- [ ] `L1` What is `retention.ms`?
- [ ] `L1` What is the high watermark?
- [ ] `L1` Name one reason **not** to use Kafka.
