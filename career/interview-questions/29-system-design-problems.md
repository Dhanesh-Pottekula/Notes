# 29. System design — full design problems

The design round is one open prompt and 45 minutes of drilling. For each problem: say the prompt back, ask the
clarifying questions below, estimate, sketch, then survive the deep dives. Concepts live in `11-system-design.md`. Syllabus: 2C System design (`../../syllabus.html`).

## 29.1 URL shortener (Bitly / TinyURL)
**Learn:** *System Design Interview* (Xu) vol1 ch8 · HelloInt breakdown "Bitly" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · https://github.com/donnemartin/system-design-primer (Pastebin solution)
### Opening
- [ ] `L1` Design a URL shortener like bit.ly.
### Clarify
- [ ] `L2` What do you ask first? ↳ custom aliases, expiry, analytics, read:write ratio, scale, deletion
- [ ] `L2` Do short links ever change destination? Do the same long URLs get the same short code?
### Estimate
- [ ] `L2` 100M new URLs a month, 100:1 reads to writes. Estimate write QPS, read QPS and 5-year storage.
- [ ] `L2` How long must the short code be for 5 years of URLs in base62? ↳ 62⁷ ≈ 3.5 trillion; 7 chars is plenty
### Deep dives
- [ ] `L2` What APIs do you expose? What does the redirect response look like? ↳ POST /urls, GET /{code}; 301 vs 302
- [ ] `L2` 301 vs 302 redirect: which do you pick and how does it affect analytics?
- [ ] `L2` How do you generate the short code? Hash vs counter vs random. ↳ hash+collision check, counter+base62, ID ranges per server
- [ ] `L2` Hashing the long URL and taking 7 chars: how do you handle collisions?
- [ ] `L2` A global counter is a bottleneck. How do you hand out ID ranges? ↳ ticket server / ZooKeeper allocates blocks per app server
- [ ] `L2` Which database do you use and what is the schema?
- [ ] `L2` How do you cache redirects? What hit ratio do you expect?
- [ ] `L2` How do you handle custom aliases and their uniqueness?
- [ ] `L2` How do you expire links and clean them up?
- [ ] `L3` Sequential codes are guessable. Why does that matter and how do you fix it? ↳ enumeration of private links; shuffle/encrypt the counter
- [ ] `L3` How do you count clicks per link without slowing the redirect? ↳ async event to queue, batch aggregate
- [ ] `L3` How do you stop the shortener being used for phishing and spam?
- [ ] `L3` One link goes viral at 500k redirects/s. What breaks and what saves you?
- [ ] `L3` How do you make this multi-region with low-latency redirects everywhere?

## 29.2 Distributed rate limiter
**Learn:** *System Design Interview* (Xu) vol1 ch4 · https://stripe.com/blog/rate-limiters · https://redis.io/learn/howtos/ratelimiting · https://blog.cloudflare.com/counting-things-a-lot-of-different-things/
### Opening
- [ ] `L1` Design a rate limiter for an API used by millions of clients.
### Clarify
- [ ] `L2` What do you clarify for the distributed rate limiter? ↳ client-side or server-side, keys (user/IP/API key), limits per endpoint, hard or soft
- [ ] `L2` Is it a library inside each service or a shared service/gateway feature?
### Estimate
- [ ] `L2` 1M active API keys, 50k requests/s. How much memory do counters need in Redis?
### Deep dives
- [ ] `L2` Compare token bucket, leaky bucket, fixed window, sliding window log, sliding window counter.
- [ ] `L2` Show the fixed-window boundary burst problem with numbers.
- [ ] `L2` Implement token bucket in Redis. Why must the check-and-decrement be atomic? ↳ Lua script or MULTI; race between GET and SET
- [ ] `L2` Where does the limiter sit: gateway, sidecar, middleware?
- [ ] `L2` What do you return to a limited client? ↳ 429, Retry-After, X-RateLimit-Remaining
- [ ] `L2` How do limit rules get configured and reloaded without deploys?
- [ ] `L3` Redis adds a network hop to every request. How do you cut latency? ↳ local token cache, batch syncs, approximate counts
- [ ] `L3` Redis is down. Fail open or fail closed? Defend it per endpoint.
- [ ] `L3` How do you rate-limit across multiple regions without a global round trip?
- [ ] `L3` How do you rate-limit LLM usage by tokens, not by requests?
- [ ] `L3` How would you add per-tenant quotas (monthly) on top of per-second limits?
- [ ] `L3` How do you test that the limiter is correct under concurrency?

## 29.3 Key-value store (Dynamo-style)
**Learn:** *System Design Interview* (Xu) vol1 ch6 · DDIA ch5 "Leaderless Replication" (pdf p193) · DDIA ch6 (pdf p213–234) · DBI ch12 (gossip, Merkle trees, pdf p381–400) · Amazon Dynamo paper (2007)
### Opening
- [ ] `L2` Design a distributed key-value store like DynamoDB or Cassandra.
### Clarify
- [ ] `L2` What do you clarify for the key-value store? ↳ value size, read/write ratio, consistency needs, latency, availability target, scale
- [ ] `L2` Strong or eventual consistency — and can the client choose per request?
### Estimate
- [ ] `L2` 10 TB of data, 3 replicas, 2 TB per node. How many nodes, and how many per partition?
### Deep dives
- [ ] `L2` How do you partition the keys? ↳ consistent hashing with virtual nodes
- [ ] `L2` How do you replicate each key? Which nodes hold the replicas?
- [ ] `L2` Walk through a write with N=3, W=2. Walk through a read with R=2.
- [ ] `L2` How do nodes learn about each other and detect failures? ↳ gossip membership, heartbeats
- [ ] `L2` What is the on-disk storage engine? Why an LSM tree? ↳ commit log, memtable, SSTables, compaction, Bloom filters
- [ ] `L2` How do you handle a node that is down for 10 minutes? ↳ sloppy quorum, hinted handoff
- [ ] `L3` Two clients write the same key concurrently on different replicas. How do you detect and resolve the conflict? ↳ vector clocks, siblings, LWW trade-off
- [ ] `L3` How do replicas that missed writes catch up? ↳ read repair, Merkle-tree anti-entropy
- [ ] `L3` How do you add a node and move data without downtime?
- [ ] `L3` How do you support TTLs and deletes? What are tombstones and why keep them?
- [ ] `L3` How do you handle a hot key that one partition cannot serve?
- [ ] `L3` How would you add a conditional write (compare-and-set) to this store?

## 29.4 Unique ID generator (Snowflake)
**Learn:** *System Design Interview* (Xu) vol1 ch7 · https://blog.x.com/engineering/en_us/a/2010/announcing-snowflake · https://medium.com/instagram-engineering/sharding-ids-at-instagram-1cf5a71e5a5c · RFC 9562 (UUIDv7)
### Opening
- [ ] `L1` Design a service that generates unique IDs across many servers.
### Clarify
- [ ] `L2` What do you clarify for the unique ID generator? ↳ size (64-bit?), sortable by time, numeric only, QPS, gaps allowed
### Estimate
- [ ] `L2` 10,000 IDs per second per machine for 1,000 machines: does a Snowflake layout fit?
### Deep dives
- [ ] `L2` Compare auto-increment DB, UUIDv4, UUIDv7, ticket server, Snowflake.
- [ ] `L2` Draw the Snowflake bit layout. ↳ 1 sign, 41 timestamp ms, 10 machine, 12 sequence
- [ ] `L2` How long until 41 bits of milliseconds run out? Why a custom epoch?
- [ ] `L2` What happens when 4,096 IDs are requested in one millisecond on one machine?
- [ ] `L2` Why are random UUIDv4 primary keys bad for B-tree indexes? ↳ random inserts, page splits, cache misses
- [ ] `L2` How are machine IDs assigned, and what happens if two machines get the same one?
- [ ] `L3` The clock moves backwards after an NTP sync. What does your generator do?
- [ ] `L3` IDs are "roughly" time-ordered across machines. Is that enough for ordering chat messages?
- [ ] `L3` How did Instagram generate IDs inside Postgres shards?
- [ ] `L3` Should IDs exposed to users reveal creation time and volume? What do you do about it?

## 29.5 Web crawler
**Learn:** *System Design Interview* (Xu) vol1 ch9 · HelloInt breakdown "Web crawler" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · DBI ch7 "Bloom Filters" (pdf p246)
### Opening
- [ ] `L2` Design a web crawler that crawls 1 billion pages a month.
### Clarify
- [ ] `L2` What do you clarify for the web crawler? ↳ purpose (search/LLM data), content types, freshness, politeness, storage duration
### Estimate
- [ ] `L2` 1B pages/month at 500 KB each: pages per second and storage per year?
### Deep dives
- [ ] `L2` Draw the web crawler pipeline. ↳ seed URLs, frontier, fetcher, DNS resolver, parser, dedupe, store, URL extractor
- [ ] `L2` What is the URL frontier and how do you prioritise URLs?
- [ ] `L2` How do you stay polite to each host? ↳ robots.txt, per-host queue, delay, one fetcher per host
- [ ] `L2` How do you avoid crawling the same URL twice? ↳ URL normalisation + Bloom filter / seen set
- [ ] `L2` How do you detect duplicate or near-duplicate content? ↳ content hash, SimHash/MinHash
- [ ] `L2` Why does DNS become a bottleneck, and how do you fix it?
- [ ] `L3` How do you avoid spider traps (infinite calendars, session URLs)?
- [ ] `L3` How do you recrawl pages based on how often they change?
- [ ] `L3` How do you distribute the frontier across 100 crawler machines and keep per-host politeness?
- [ ] `L3` A worker crashes mid-crawl. How do you not lose or double-crawl its URLs?
- [ ] `L3` How do you crawl JavaScript-heavy pages? What does it cost?

## 29.6 Notification system
**Learn:** *System Design Interview* (Xu) vol1 ch10 · DDIA ch11 (notification delivery as streams) · https://firebase.google.com/docs/cloud-messaging · https://developer.apple.com/documentation/usernotifications
### Opening
- [ ] `L2` Design a notification system that sends push, SMS and email.
### Clarify
- [ ] `L2` What do you clarify for the notification system? ↳ channels, volume, realtime vs scheduled, preferences, opt-out, priority, rate limits
### Estimate
- [ ] `L2` 10M push, 1M SMS and 5M emails a day. Peak QPS per channel?
### Deep dives
- [ ] `L2` Draw the flow from "event happened" to "phone buzzes". ↳ API, validation, prefs, template, per-channel queue, workers, provider
- [ ] `L2` Why a separate queue and worker pool per channel?
- [ ] `L2` How do you store and respect user preferences and quiet hours?
- [ ] `L2` How do templates and localisation work?
- [ ] `L2` A provider (SMS vendor) fails. Retries, backoff, failover to second vendor?
- [ ] `L2` How do you avoid sending the same notification twice? ↳ dedupe key per event+user, idempotent workers
- [ ] `L2` How do you track delivered, opened, clicked?
- [ ] `L3` A marketing blast to 50M users must not delay OTP messages. How? ↳ priority queues, separate pools, rate limits per tier
- [ ] `L3` How do you rate-limit notifications per user so you don't spam them?
- [ ] `L3` How do you handle device token expiry and uninstalls?
- [ ] `L3` How do you send scheduled notifications at the user's local 9 am across time zones?

## 29.7 News feed / timeline (Twitter, Instagram, LinkedIn)
**Learn:** DDIA ch1 "Describing load" — Twitter fan-out (pdf p31–35) · *System Design Interview* (Xu) vol1 ch11 · https://www.infoq.com/presentations/Twitter-Timeline-Scalability/ · HelloInt breakdown "News feed" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview)
### Opening
- [ ] `L2` Design a news feed like Twitter's home timeline.
### Clarify
- [ ] `L2` What do you clarify for the news feed? ↳ follow graph size, ranking or chronological, media, feed freshness, DAU, posts/day
### Estimate
- [ ] `L2` 300M DAU, 2 posts/day, 200 follows each, feed opened 10 times a day. Write QPS, read QPS, fan-out writes?
### Deep dives
- [ ] `L2` Fan-out on write (push) vs fan-out on read (pull): explain both and their costs.
- [ ] `L2` How do you handle a celebrity with 100M followers? ↳ hybrid: push for normal users, pull celebrities at read time
- [ ] `L2` What does the feed cache look like? ↳ Redis list of post IDs per user, capped length
- [ ] `L2` How do you paginate a feed that changes while scrolling? ↳ cursor by ID/time, not offset
- [ ] `L2` How do you store posts, follows and media? Which databases?
- [ ] `L2` How do you count likes on a post with 1M likes a minute? ↳ sharded counters, batched increments
- [ ] `L3` How do you skip fan-out for inactive users?
- [ ] `L3` How do you add a ranking model to the feed without making it slow? ↳ candidate generation, lightweight rank, precompute features
- [ ] `L3` A user unfollows someone. How fast do their posts disappear from the feed?
- [ ] `L3` A user deletes a post that is already fanned out to 5M feeds. What do you do?
- [ ] `L3` How do you insert ads into the feed?
- [ ] `L3` How do you make the feed load in under 200 ms at p99?

## 29.8 Chat app (WhatsApp / Slack / Messenger)
**Learn:** *System Design Interview* (Xu) vol1 ch12 · HelloInt breakdown "WhatsApp" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · https://discord.com/blog/how-discord-stores-trillions-of-messages · https://slack.engineering/real-time-messaging/
### Opening
- [ ] `L2` Design a chat app like WhatsApp with 1:1 and group chats.
### Clarify
- [ ] `L2` What do you clarify for the chat app? ↳ 1:1 vs groups (size), media, read receipts, history length, E2E encryption, multi-device
- [ ] `L2` Slack-style channels vs WhatsApp-style groups: what changes in the design?
### Estimate
- [ ] `L2` 500M DAU, 40 messages/day each, 100 bytes each. Messages per second, storage per year, concurrent connections?
### Deep dives
- [ ] `L2` How do clients connect, and why WebSockets? ↳ persistent bidirectional, low latency; fallback long polling
- [ ] `L2` Walk a message from sender to receiver when both are online on different servers. ↳ connection registry, pub/sub or routing service
- [ ] `L2` The receiver is offline. How is the message delivered later? ↳ store in DB/inbox, push notification, sync on reconnect
- [ ] `L2` How do you store messages? Which database and which partition key? ↳ wide-column, partition by conversation id, cluster by message id
- [ ] `L2` How do you guarantee message order inside a conversation?
- [ ] `L2` Sent, delivered, read ticks: how do you implement them?
- [ ] `L2` How do clients sync history across multiple devices?
- [ ] `L2` How do you send media (photos, voice notes)? ↳ upload to blob via presigned URL, send pointer
- [ ] `L2` How does group messaging fan out to 1,000 members?
- [ ] `L3` How do you avoid duplicate messages when the client retries a send? ↳ client-generated message id, idempotent insert
- [ ] `L3` How do you keep a per-conversation sequence number without a global lock?
- [ ] `L3` A chat server with 100k connections crashes. What happens to those users and in-flight messages?
- [ ] `L3` How does end-to-end encryption change what the server can do? ↳ server can't search/index; key exchange, Signal protocol
- [ ] `L3` How do you design a 100k-member channel (Slack/Discord) differently from a 10-person group?
- [ ] `L3` How do you search message history?
- [ ] `L3` What parts of AiRA's WebSocket setup would you reuse for this chat app, and what would break at WhatsApp scale?

## 29.9 Presence / online status
**Learn:** https://slack.engineering/real-time-messaging/ · https://discord.com/blog (presence posts) · *System Design Interview* (Xu) vol1 ch12 "Online presence" · Xu vol2 ch2 "Nearby Friends"
### Opening
- [ ] `L2` Design the "online / last seen" indicator for a chat app.
### Clarify
- [ ] `L2` What do you clarify for presence / online status? ↳ freshness needed, who can see it, idle vs offline, multi-device, privacy settings
### Estimate
- [ ] `L2` 100M online users sending a heartbeat every 30 s: what QPS hits the presence service?
### Deep dives
- [ ] `L2` Heartbeats vs connection open/close events: which do you trust and why?
- [ ] `L2` Where do you store presence? ↳ Redis with TTL keys, refreshed by heartbeat
- [ ] `L2` How do you tell friends that a user went online without a storm of messages?
- [ ] `L2` How do you handle flapping on bad mobile networks? ↳ grace period before marking offline
- [ ] `L2` A user is online on phone and laptop. How do you combine their status?
- [ ] `L2` What APIs and events does the presence service expose?
- [ ] `L3` A user with 5,000 friends goes online. How do you fan out cheaply? ↳ only to online friends, lazy fetch on open, subscriptions
- [ ] `L3` How do you show presence in a 100k-member Slack channel?
- [ ] `L3` What consistency do you need for presence, and why is "approximately right" fine?
- [ ] `L3` How do you respect privacy settings like "hide last seen" during fan-out?

## 29.10 Search autocomplete / typeahead
**Learn:** *System Design Interview* (Xu) vol1 ch13 · HelloInt breakdown "Top-K" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · https://www.elastic.co/guide/en/elasticsearch/reference/current/search-suggesters.html
### Opening
- [ ] `L2` Design search autocomplete that shows the top 5 suggestions as the user types.
### Clarify
- [ ] `L2` What do you clarify for typeahead? ↳ ranking signal, personalised or global, languages, freshness/trending, latency target
### Estimate
- [ ] `L2` 10M DAU, 10 searches each, 20 keystrokes per search. Autocomplete QPS?
### Deep dives
- [ ] `L2` Why a trie, and what does each node store? ↳ prefix nodes with cached top-k completions
- [ ] `L2` How do you build the trie from query logs? How often?
- [ ] `L2` How do you shard the trie when it does not fit on one machine?
- [ ] `L2` How do you cut requests from the browser? ↳ debounce, client cache, CDN cache for popular prefixes
- [ ] `L2` How do you meet a 100 ms p99 budget end to end?
- [ ] `L3` How do you add trending queries in near real time? ↳ streaming counts, separate fresh trie, merge
- [ ] `L3` How do you filter offensive or unsafe suggestions?
- [ ] `L3` How do you personalise suggestions without a per-user trie?
- [ ] `L3` How do you handle typos in the prefix?
- [ ] `L3` Trie in memory vs Elasticsearch completion suggester vs Redis sorted sets: trade-offs.

## 29.11 Video streaming (YouTube / Netflix)
**Learn:** *System Design Interview* (Xu) vol1 ch14 · HelloInt breakdown "YouTube" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · https://netflixtechblog.com (Open Connect, encoding posts)
### Opening
- [ ] `L2` Design YouTube: upload and watch videos.
### Clarify
- [ ] `L2` What do you clarify for video streaming? ↳ upload vs watch focus, video length/size, devices, live or VOD, global users
### Estimate
- [ ] `L2` 500 hours uploaded per minute, 1B views a day at ~5 Mbps. Storage per day and peak egress?
### Deep dives
- [ ] `L2` Walk through the upload path. ↳ presigned multipart upload, raw blob, transcode queue, outputs, metadata update
- [ ] `L2` What is transcoding and why produce many resolutions and codecs?
- [ ] `L2` How does the transcoding pipeline split work? ↳ split into segments, DAG of tasks, parallel workers
- [ ] `L2` What is adaptive bitrate streaming (HLS / DASH) and how does the player switch quality?
- [ ] `L2` Why serve video from a CDN, and what does the origin still do?
- [ ] `L2` How do you store video metadata, view counts and comments?
- [ ] `L3` How do you resume a failed 4 GB upload on a mobile network?
- [ ] `L3` Popular vs long-tail videos: how do you decide what to keep on edge caches?
- [ ] `L3` How do you count views accurately at billions per day without hammering the DB?
- [ ] `L3` How do you cut transcoding cost for videos nobody watches?
- [ ] `L3` What changes for live streaming vs video on demand?
- [ ] `L3` How do you protect paid content? ↳ signed URLs, DRM, token-authenticated segments

## 29.12 File storage and sync (Dropbox / Google Drive)
**Learn:** *System Design Interview* (Xu) vol1 ch15 · HelloInt breakdown "Dropbox" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · https://dropbox.tech/infrastructure/streaming-file-synchronization
### Opening
- [ ] `L2` Design Dropbox / Google Drive with sync across devices.
### Clarify
- [ ] `L2` What do you clarify for file storage and sync? ↳ max file size, sharing, versioning, offline edits, conflict handling, devices per user
### Estimate
- [ ] `L2` 50M users, 10 GB each on average, 10% daily active editing 5 files: storage and upload traffic?
### Deep dives
- [ ] `L2` Why split files into chunks? How big should chunks be?
- [ ] `L2` How does chunk-level dedupe work? ↳ content hash per chunk, store once, reference count
- [ ] `L2` What goes in the metadata DB vs blob storage?
- [ ] `L2` How does a client learn that a file changed on another device? ↳ long poll / WebSocket notification, then delta sync
- [ ] `L2` How do you upload only the changed parts of a large file?
- [ ] `L2` How do you implement file versioning and restore?
- [ ] `L3` Two devices edit the same file offline. How do you resolve the conflict? ↳ detect via version; keep both as "conflicted copy"
- [ ] `L3` How do you share a folder with 1,000 people and keep permissions fast to check?
- [ ] `L3` How do you garbage-collect chunks no longer referenced by any file version?
- [ ] `L3` Should the client encrypt files before upload? What do you lose if it does?

## 29.13 Ride hailing (Uber / Ola) with geo-indexing
**Learn:** HelloInt breakdown "Uber" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · *System Design Interview* (Xu) vol2 ch1 "Proximity Service", ch2 "Nearby Friends" · https://www.uber.com/blog/h3/
### Opening
- [ ] `L2` Design Uber: riders request rides, nearby drivers get matched.
### Clarify
- [ ] `L2` What do you clarify for ride hailing? ↳ matching latency, location update frequency, pricing/surge scope, payments in scope, cities
### Estimate
- [ ] `L2` 5M active drivers sending location every 4 seconds. Write QPS on the location service?
### Deep dives
- [ ] `L2` How do you store and query live driver locations? ↳ in-memory geo index (Redis GEO / H3 cells), not the main DB
- [ ] `L2` Geohash vs quadtree vs H3 for this use case: which and why?
- [ ] `L2` Find drivers within 2 km of a rider. Walk through the query.
- [ ] `L2` How do you match a rider to a driver and stop two riders getting the same driver? ↳ driver lock with TTL, offer one driver at a time
- [ ] `L2` The driver doesn't accept within 10 seconds. What happens?
- [ ] `L2` How does the rider see the driver moving on the map in real time?
- [ ] `L2` What is the trip state machine? ↳ requested, matched, arriving, in progress, completed, cancelled
- [ ] `L3` How do you shard the location index by geography, and what about city boundaries?
- [ ] `L3` How do you compute ETA, and why not just straight-line distance?
- [ ] `L3` How does surge pricing work as a system (inputs, frequency, consistency)?
- [ ] `L3` A region's location service dies. What do riders and drivers see?
- [ ] `L3` How do you keep trip records correct when the driver's phone loses network mid-trip?

## 29.14 Food delivery (Swiggy / Zomato) — tie to StreetDine
**Learn:** https://bytes.swiggy.com · https://blog.zomato.com/category/technology · HelloInt breakdown "Uber" (dispatch ideas) · DDIA ch11 (order events as streams)
### Opening
- [ ] `L2` Design Swiggy/Zomato: browse restaurants, order food, track delivery.
### Clarify
- [ ] `L2` What do you clarify for food delivery? ↳ cities, restaurant integration, delivery partners, live tracking, payments, peak hours
### Estimate
- [ ] `L2` 2M orders a day with 3× dinner peak. Order QPS at peak, and location updates from 300k riders?
### Deep dives
- [ ] `L2` What services do you split into? ↳ catalogue/menu, search, cart, order, payment, dispatch, tracking, notifications
- [ ] `L2` What is the order state machine, and who moves each transition?
- [ ] `L2` How does the restaurant receive and accept an order reliably (tablet offline)?
- [ ] `L2` How do you show "restaurants open now that deliver to me" fast? ↳ geo index + serviceability polygons + cache
- [ ] `L2` How do you handle menu item availability changes during the dinner rush?
- [ ] `L2` How do you assign a delivery partner? What do you optimise?
- [ ] `L2` How does live order tracking reach the customer's app?
- [ ] `L3` Payment succeeded but order creation failed. What does the customer see and how do you fix it? ↳ idempotency, saga, auto-refund, reconciliation
- [ ] `L3` How do you batch two orders to one rider?
- [ ] `L3` How do you compute the delivery-time promise shown before ordering?
- [ ] `L3` What did StreetDine's ordering flow look like, and what would you change for 100× scale?

## 29.15 Ticket booking (BookMyShow / Ticketmaster) with seat locking
**Learn:** HelloInt breakdown "Ticketmaster" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · DDIA ch7 "Preventing Lost Updates" (pdf p255) · https://redis.io/docs/latest/develop/use/patterns/distributed-locks/
### Opening
- [ ] `L2` Design BookMyShow: pick a show, choose seats, pay.
### Clarify
- [ ] `L2` What do you clarify for ticket booking? ↳ seat map vs general admission, hold time, popular-event spikes, payment flow, cancellations
### Estimate
- [ ] `L2` A big release opens bookings: 5M users in 10 minutes for 200k seats. Peak QPS on seat selection?
### Deep dives
- [ ] `L2` How do you stop two users booking the same seat? ↳ row lock / conditional update / unique constraint
- [ ] `L2` How do you hold seats for 10 minutes while the user pays? ↳ status=held with expiry; Redis TTL lock; release job
- [ ] `L2` Pessimistic vs optimistic locking for seat holds: which and why?
- [ ] `L2` What happens when the hold expires while payment is in progress?
- [ ] `L2` How do you show the live seat map to thousands of viewers?
- [ ] `L2` What is the booking state machine?
- [ ] `L3` How do you survive a flash crowd for a blockbuster? ↳ virtual waiting room, admission tokens, queue
- [ ] `L3` Redis holds the seat lock but Postgres is the source of truth. What if they disagree?
- [ ] `L3` Payment gateway times out. Did the user pay? How do you reconcile?
- [ ] `L3` How do you stop bots from grabbing all seats?

## 29.16 Payment system and wallet (incl. UPI-like flow)
**Learn:** *System Design Interview* (Xu) vol2 ch11 "Payment System", ch12 "Digital Wallet" · https://stripe.com/blog/ledger-stripe-system-for-tracking-and-validating-money-movement · https://stripe.com/blog/idempotency · https://www.npci.org.in/what-we-do/upi/product-overview
### Opening
- [ ] `L2` Design a payment system for an e-commerce site.
- [ ] `L2` Design a digital wallet where users top up and pay each other.
### Clarify
- [ ] `L2` What do you clarify for the payment system? ↳ own processing or PSP (Stripe/Razorpay), refunds, currencies, payouts, compliance
- [ ] `L2` What correctness guarantees does money need that a feed does not?
### Estimate
- [ ] `L2` 1M payments a day: average and peak TPS? Why is throughput rarely the hard part here?
### Deep dives
- [ ] `L2` Walk the pay-in flow from "Pay" button to order confirmed. ↳ payment intent, PSP hosted page, webhook, ledger, order update
- [ ] `L2` What is an idempotency key and where exactly is it checked?
- [ ] `L2` What is double-entry bookkeeping and why use a ledger? ↳ every movement = debit + credit, sums to zero, append-only
- [ ] `L2` Why are ledger entries immutable? How do you correct a mistake?
- [ ] `L2` How do you handle PSP webhooks that arrive late, twice, or out of order?
- [ ] `L2` Why store money as integers in minor units, never floats?
- [ ] `L2` What is the payment state machine?
- [ ] `L2` How does a UPI payment flow work at a high level? ↳ PSP app, NPCI switch, issuer/acquirer banks, collect vs intent
- [ ] `L3` What is reconciliation, and how do you run it against the PSP's settlement files?
- [ ] `L3` The PSP call timed out. Did money move? What does your system do next? ↳ unknown state, query status, never blind retry
- [ ] `L3` Wallet transfer A → B: how do you keep balances correct under concurrent transfers? ↳ single DB txn, row locks in fixed order, or ledger
- [ ] `L3` How do you shard a wallet ledger when one transfer touches two shards?
- [ ] `L3` How would you design wallet balances with event sourcing?
- [ ] `L3` How do you handle refunds and partial refunds?
- [ ] `L3` What do you log and encrypt for PCI-DSS? Why never store card numbers?
- [ ] `L3` How do you detect fraud without blocking the payment path?

## 29.17 E-commerce checkout, inventory and flash sales
**Learn:** HelloInt breakdown "Ticketmaster" (contention ideas) · https://microservices.io/patterns/data/saga.html · https://tech-blog.flipkart.net · DDIA ch7 "Preventing Lost Updates" (pdf p255)
### Opening
- [ ] `L2` Design the checkout and inventory system for an e-commerce site.
- [ ] `L2` Design Flipkart's flash sale for 10M users and 10k items.
### Clarify
- [ ] `L2` What do you clarify for the e-commerce checkout? ↳ multi-warehouse, reservation window, payment methods, cart persistence, oversell tolerance
### Estimate
- [ ] `L2` 10M users hit "buy" in the first minute of a sale. Peak QPS and how much hits the DB?
### Deep dives
- [ ] `L2` How do you prevent overselling? ↳ atomic conditional decrement (`stock > 0`), reservation rows, Redis DECR + DB truth
- [ ] `L2` Reserve stock at add-to-cart, at checkout, or at payment? Trade-offs.
- [ ] `L2` What saga runs on checkout, and what are its compensations?
- [ ] `L2` How do you release reservations when the user abandons payment?
- [ ] `L2` Where does the cart live (Redis, DB, client) and why?
- [ ] `L3` One hot item gets 1M requests/s. How do you keep the stock counter from melting? ↳ pre-split stock buckets, Redis Lua, queue buyers
- [ ] `L3` How do you put users in a virtual queue and admit them fairly?
- [ ] `L3` How do you keep inventory consistent across warehouses and channels (app, web, marketplace)?
- [ ] `L3` What do you degrade first when the sale overloads the system?
- [ ] `L3` How do you test a flash sale design before the real event? ↳ load tests with real traffic shape, game days

## 29.18 Distributed job scheduler / cron — tie to AiRA reminders
**Learn:** HelloInt breakdown "Job scheduler" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · DDIA ch8 "The truth is defined by the majority" (pdf p314) · https://docs.temporal.io/ · https://slack.engineering/executing-cron-scripts-reliably-at-scale/
### Opening
- [ ] `L2` Design a distributed job scheduler that runs one-off and recurring jobs at a given time.
### Clarify
- [ ] `L2` What do you clarify for the job scheduler? ↳ precision (seconds/minutes), job count, at-most vs at-least-once, job duration, retries
### Estimate
- [ ] `L2` 100M scheduled reminders, 10% firing in the morning hour. Peak jobs per second?
### Deep dives
- [ ] `L2` How do you store jobs so "what is due now?" is cheap? ↳ index on next_run_at, time buckets, Redis sorted set
- [ ] `L2` Polling the DB vs a delay queue vs timing wheel: trade-offs.
- [ ] `L2` How do many workers pick jobs without two running the same job? ↳ SKIP LOCKED, leases, claim with status update
- [ ] `L2` What is a lease and what happens when a worker dies mid-job?
- [ ] `L2` How do you compute the next run of a cron expression with time zones and DST?
- [ ] `L2` How do retries, backoff and a DLQ fit in?
- [ ] `L3` At-least-once vs at-most-once for reminders: which did AiRA choose and why? ↳ at-most-once via Redis locks; duplicate reminders worse than rare miss
- [ ] `L3` How do you make job execution idempotent when a lease expires but the old worker still finishes?
- [ ] `L3` How do you avoid a thundering herd at exactly 9:00:00?
- [ ] `L3` How do you scale the scheduler itself? Partition jobs by what?
- [ ] `L3` How do you let users see job history and logs?
- [ ] `L3` When would you use Temporal / Celery beat / cloud schedulers instead of building this?

## 29.19 Metrics and monitoring system (Prometheus / Datadog)
**Learn:** *System Design Interview* (Xu) vol2 ch5 "Metrics Monitoring and Alerting System" · https://prometheus.io/docs/introduction/overview/ · http://www.vldb.org/pvldb/vol8/p1816-teller.pdf (Gorilla)
### Opening
- [ ] `L2` Design a metrics monitoring and alerting system.
### Clarify
- [ ] `L2` What do you clarify for the metrics system? ↳ number of hosts/series, resolution, retention, query patterns, alert latency
### Estimate
- [ ] `L2` 100k hosts × 500 metrics every 10 s: data points per second and storage per day?
### Deep dives
- [ ] `L2` Push vs pull collection: trade-offs. ↳ Prometheus pulls; push for short-lived jobs and firewalls
- [ ] `L2` What is a time series, and what are labels / cardinality?
- [ ] `L2` Why a time-series database instead of Postgres? How is the data compressed? ↳ delta-of-delta timestamps, XOR floats
- [ ] `L2` What is downsampling and retention tiering?
- [ ] `L2` How does alert evaluation work, and how do you avoid alert storms? ↳ rules engine, for-duration, grouping, dedupe, silences
- [ ] `L2` What does the query language need to support (rate, sum by label, percentiles)?
- [ ] `L3` A team adds a `user_id` label. What happens to the system?
- [ ] `L3` How do you make the monitoring system itself highly available? Who monitors the monitor?
- [ ] `L3` How do you shard ingestion and queries across many TSDB nodes?
- [ ] `L3` How do you compute p99 across 1,000 servers correctly? ↳ histograms/sketches merged, not averaged percentiles

## 29.20 Logging pipeline (ELK / Loki)
**Learn:** https://www.elastic.co/guide/en/observability/current/logs-observability-overview.html · https://grafana.com/docs/loki/latest/get-started/overview/ · https://opentelemetry.io/docs/concepts/signals/logs/
### Opening
- [ ] `L2` Design a centralised logging system for 2,000 services.
### Clarify
- [ ] `L2` What do you clarify for the logging pipeline? ↳ volume, retention, search needs, structured or not, PII, cost ceiling
### Estimate
- [ ] `L2` 5 TB of logs a day, 30 days hot, 1 year cold. Storage and ingest rate?
### Deep dives
- [ ] `L2` Draw the logging pipeline. ↳ agent (Fluent Bit), buffer (Kafka), processors, index/store, query UI
- [ ] `L2` Why put Kafka between agents and the index?
- [ ] `L2` Full-text index everything (Elasticsearch) vs index labels only (Loki): trade-offs.
- [ ] `L2` How do you correlate logs with traces? ↳ trace id in every log line
- [ ] `L2` How do you redact PII and secrets from logs?
- [ ] `L2` Structured (JSON) vs plain-text logs: why does it matter for the pipeline?
- [ ] `L3` Log volume spikes 10× during an incident — exactly when you need logs. How do you cope? ↳ buffering, sampling debug logs, priority, backpressure
- [ ] `L3` How do you keep costs down? ↳ sampling, levels, tiered storage, drop noisy logs, metrics instead
- [ ] `L3` How do you make "search last 15 minutes across all services" fast?
- [ ] `L3` How do you enforce retention and deletion for compliance across hot and cold tiers?

## 29.21 Leaderboard
**Learn:** *System Design Interview* (Xu) vol2 ch10 "Real-time Gaming Leaderboard" · https://redis.io/docs/latest/develop/data-types/sorted-sets/
### Opening
- [ ] `L1` Design a real-time leaderboard for a game with 50M players.
### Clarify
- [ ] `L2` What do you clarify for the leaderboard? ↳ global vs friends vs regional, time windows (daily/all-time), ties, update rate
### Estimate
- [ ] `L2` 5M daily players, 10 score updates each. Update QPS and sorted-set memory?
### Deep dives
- [ ] `L2` Why a Redis sorted set? What are the costs of ZADD, ZREVRANK, ZREVRANGE? ↳ O(log n) skip list
- [ ] `L2` How do you get a player's rank and the 5 players around them?
- [ ] `L2` How do you do daily and weekly leaderboards? ↳ one key per period, expire old keys
- [ ] `L2` How do you break ties fairly? ↳ composite score: points + inverse timestamp
- [ ] `L2` Where is the durable copy of scores, and how do you rebuild Redis after loss?
- [ ] `L2` What APIs do you expose: submit score, top N, my rank?
- [ ] `L3` 500M players don't fit in one sorted set. How do you shard and still answer "what is my rank?" ↳ score-range shards with counts, or approximate rank
- [ ] `L3` How do you show a friends-only leaderboard efficiently?
- [ ] `L3` How do you stop cheaters from posting fake scores?
- [ ] `L3` How do you handle a season reset at midnight for 50M players?

## 29.22 Proximity service (Yelp / Google Places nearby)
**Learn:** *System Design Interview* (Xu) vol2 ch1 "Proximity Service" · https://www.movable-type.co.uk/scripts/geohash.html · https://postgis.net/documentation/ · https://h3geo.org/docs/
### Opening
- [ ] `L2` Design "find restaurants near me" like Yelp.
### Clarify
- [ ] `L2` What do you clarify for the proximity service? ↳ radius, filters (open now, rating), business update rate, read QPS, map view vs list
### Estimate
- [ ] `L2` 100M DAU, 5 searches each, 200M businesses. Search QPS and index size?
### Deep dives
- [ ] `L2` Why can't you just index latitude and longitude separately?
- [ ] `L2` Geohash: how does precision map to cell size, and how do you search a radius? ↳ prefix length; query cell + 8 neighbours
- [ ] `L2` Quadtree: how is it built and when does a node split?
- [ ] `L2` Business data changes rarely but reads are huge. How does that shape the design? ↳ read replicas, cache, rebuild index offline
- [ ] `L2` PostGIS vs Redis GEO vs Elasticsearch geo queries: when each?
- [ ] `L2` Business owners edit listings. How fast must changes appear, and how do they flow?
- [ ] `L3` How do you rank results by distance, rating and relevance together?
- [ ] `L3` How do you handle the edge where two nearby points have very different geohashes?
- [ ] `L3` How would you serve "nearby friends" where both sides move?
- [ ] `L3` How do you shard the geo index across regions and countries?

## 29.23 Collaborative editing (Google Docs) — OT and CRDTs
**Learn:** HelloInt breakdown "Google Docs" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · DBI ch11 "Strong Eventual Consistency and CRDTs" (pdf p375) · https://www.figma.com/blog/how-figmas-multiplayer-technology-works/ · https://crdt.tech
### Opening
- [ ] `L2` Design Google Docs: many users editing the same document at the same time.
### Clarify
- [ ] `L2` What do you clarify for collaborative editing? ↳ concurrent editors per doc, offline editing, rich text, comments, history, latency
### Estimate
- [ ] `L2` 10M docs edited a day, average 3 editors, 1 op/second each while typing. Ops per second?
### Deep dives
- [ ] `L2` Why does naive "last write wins" on the whole document fail?
- [ ] `L2` What is Operational Transformation (OT)? Give a two-user insert example.
- [ ] `L2` What is a CRDT and how does it avoid a central transformer?
- [ ] `L2` OT vs CRDT: trade-offs for a server-based product.
- [ ] `L2` How do edits flow: client → server → other clients? ↳ WebSocket per doc session, server sequences ops, broadcasts
- [ ] `L2` How do you show other users' cursors and presence?
- [ ] `L3` Why route all editors of one document to the same server? What if it dies?
- [ ] `L3` How do you store the document: snapshots plus an operation log?
- [ ] `L3` How does offline editing merge back when the user reconnects?
- [ ] `L3` How do you implement version history and "restore this version"?
- [ ] `L3` How do permissions change mid-session (someone loses edit access)?

## 29.24 Stock exchange / order matching engine
**Learn:** *System Design Interview* (Xu) vol2 ch13 "Stock Exchange" · https://martinfowler.com/articles/lmax.html · DDIA ch9 "Total Order Broadcast" (pdf p360)
### Opening
- [ ] `L2` Design a stock exchange order matching system.
### Clarify
- [ ] `L2` What do you clarify for the stock exchange? ↳ order types (limit/market/cancel), symbols count, latency target, fairness, market data fan-out
### Estimate
- [ ] `L2` 10k symbols, 1M orders per second at peak. What does one matching engine per symbol need to sustain?
### Deep dives
- [ ] `L2` What is an order book? How is it structured in memory? ↳ price levels (sorted map), FIFO queue per level
- [ ] `L2` Walk through matching a market buy against the book. ↳ price-time priority
- [ ] `L2` Why is the matching engine single-threaded per symbol?
- [ ] `L2` What is the sequencer and why does everything go through it?
- [ ] `L2` How do you publish market data (ticks, depth) to thousands of subscribers?
- [ ] `L2` How do you handle cancel and modify requests that race with matches?
- [ ] `L3` How do you make the matching engine fault tolerant without slowing it? ↳ event-sourced input log, deterministic replay, hot standby
- [ ] `L3` Where do microseconds go, and why do exchanges avoid GC, locks and the network stack?
- [ ] `L3` How do pre-trade risk checks fit in without adding latency?
- [ ] `L3` How is a broker's order system (like Zerodha's) different from the exchange itself?

## 29.25 Ad click event aggregation
**Learn:** *System Design Interview* (Xu) vol2 ch6 "Ad Click Event Aggregation" · DDIA ch11 "Reasoning About Time" (pdf p474), "Fault Tolerance" (pdf p482)
### Opening
- [ ] `L2` Design a system that counts ad clicks per ad per minute for billing and dashboards.
### Clarify
- [ ] `L2` What do you clarify for ad click aggregation? ↳ freshness, accuracy for billing, late events, query dimensions, retention
### Estimate
- [ ] `L2` 1B clicks a day, 3× peak. Events per second, and raw storage per day at 100 bytes each?
### Deep dives
- [ ] `L2` Draw the click aggregation pipeline. ↳ click log → Kafka → stream aggregator → OLAP store; raw to data lake
- [ ] `L2` Tumbling windows on event time: how do you handle late clicks? ↳ watermarks, allowed lateness, correction updates
- [ ] `L2` How do you get exactly-once counts when the aggregator restarts?
- [ ] `L2` How do you deduplicate repeated clicks from the same user?
- [ ] `L2` What does the aggregated table look like (keys, columns, granularity)?
- [ ] `L3` How do you reconcile the streaming result with a nightly batch recompute? ↳ lambda-style check; batch is source of truth for billing
- [ ] `L3` How do you handle a hot ad receiving 30% of clicks?
- [ ] `L3` How do you detect click fraud in the pipeline?
- [ ] `L3` Which store serves "clicks per ad per minute, filtered by country"? ↳ ClickHouse/Druid/Pinot, pre-aggregated rollups
- [ ] `L3` You find a bug in the aggregator. How do you recompute last week's numbers? ↳ replay raw events from Kafka / data lake

## 29.26 Hotel reservation (Booking.com / Airbnb)
**Learn:** *System Design Interview* (Xu) vol2 ch7 "Hotel Reservation System" · DDIA ch7 "Preventing Lost Updates" (pdf p255), "Write Skew and Phantoms" (pdf p259)
### Opening
- [ ] `L2` Design a hotel reservation system.
### Clarify
- [ ] `L2` What do you clarify for hotel reservation? ↳ room types vs specific rooms, overbooking policy, date ranges, cancellations, payment timing
### Estimate
- [ ] `L2` 5,000 hotels, 1M rooms, 70% occupancy, 3-night stays. Reservations per second? Why is this small?
### Deep dives
- [ ] `L2` Model room inventory per room type per date. Why per date? ↳ row per (hotel, type, date) with total and reserved
- [ ] `L2` How do you reserve a 3-night stay atomically?
- [ ] `L2` How do you prevent double booking under concurrency? ↳ conditional update `reserved < total`, optimistic version, constraint
- [ ] `L2` A user clicks "Book" twice. How do you not create two reservations?
- [ ] `L2` What APIs do you expose for search, hold and confirm?
- [ ] `L2` How do you release held rooms when payment never completes?
- [ ] `L3` How do you allow 10% overbooking safely?
- [ ] `L3` How do search (availability for dates) and booking stay consistent when search is cached?
- [ ] `L3` How do you sync inventory with external channels (OTAs) that also sell your rooms?
- [ ] `L3` How would you shard reservation data, and why might one Postgres primary be enough?

## 29.27 Email service (Gmail-like)
**Learn:** *System Design Interview* (Xu) vol2 ch8 "Distributed Email Service" · https://www.cloudflare.com/learning/email-security/dmarc-dkim-spf/
### Opening
- [ ] `L2` Design an email service like Gmail: send, receive, search, folders.
### Clarify
- [ ] `L2` What do you clarify for the email service? ↳ users, attachments, search, spam filtering, threads, retention, IMAP support
### Estimate
- [ ] `L2` 1B users, 40 emails received a day at 50 KB average. Storage per day?
### Deep dives
- [ ] `L2` How does sending work end to end? ↳ SMTP outbound queue, MX lookup, retries, bounces
- [ ] `L2` How does receiving work? ↳ SMTP inbound, spam/virus checks, store, index, notify client
- [ ] `L2` How do you store emails and attachments? ↳ metadata DB partitioned by user, bodies/attachments in blob
- [ ] `L2` How do you implement threads / conversations?
- [ ] `L2` How do you search a user's mailbox fast? ↳ per-user inverted index
- [ ] `L2` How do clients see new mail instantly? ↳ WebSocket / long poll, IMAP IDLE, mobile push
- [ ] `L3` What are SPF, DKIM and DMARC and why does your outbound pipeline care?
- [ ] `L3` How do you protect sender reputation (IP warmup, rate limits per domain)?
- [ ] `L3` How do you dedupe a large attachment sent to 10,000 recipients?
- [ ] `L3` How do you shard mailboxes, and what about one user with 10M emails?

## 29.28 Distributed cache (Memcached / Redis Cluster)
**Learn:** HelloInt breakdown "Distributed cache" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/ · https://www.usenix.org/conference/nsdi13/technical-sessions/presentation/nishtala (Facebook memcache) · DBI ch5 "Page Replacement" (pdf p151)
### Opening
- [ ] `L2` Design a distributed in-memory cache.
### Clarify
- [ ] `L2` What do you clarify for the distributed cache? ↳ data size, hit latency, eviction, persistence, consistency with DB, multi-region
### Estimate
- [ ] `L2` 2 TB of hot data, 1M ops/s, 64 GB nodes. How many nodes with replication?
### Deep dives
- [ ] `L2` How do clients find the node for a key? ↳ consistent hashing in client, or hash slots (Redis Cluster 16,384)
- [ ] `L2` How do you implement LRU in O(1)? ↳ hash map + doubly linked list
- [ ] `L2` Replication and failover for cache nodes: worth it or not?
- [ ] `L2` What happens to hit rate when you add a node?
- [ ] `L2` How do you expire millions of keys with TTLs efficiently? ↳ lazy expiry on read + periodic sampling
- [ ] `L3` How do you handle a hot key that one node cannot serve?
- [ ] `L3` How did Facebook's memcache use leases to fix stale sets and thundering herds?
- [ ] `L3` How do you keep caches in two regions consistent with one primary DB?
- [ ] `L3` How do you handle large values (1 MB+) and memory fragmentation?
- [ ] `L3` How do you resize the cache cluster without a stampede on the database?

## 29.29 Distributed message queue (Kafka-like)
**Learn:** *System Design Interview* (Xu) vol2 ch4 "Distributed Message Queue" · DDIA ch11 "Partitioned Logs" (pdf p454) · see `12-kafka.md`
### Opening
- [ ] `L2` Design a distributed message queue like Kafka.
### Clarify
- [ ] `L2` What do you clarify for the distributed message queue? ↳ ordering, delivery guarantee, retention, throughput, message size, replay
### Estimate
- [ ] `L2` 1M messages/s at 1 KB, 7 days retention, RF=3. Disk and network per broker for 30 brokers?
### Deep dives
- [ ] `L2` Why an append-only log on disk, and why is it fast?
- [ ] `L2` How do topics split into partitions and where is ordering guaranteed?
- [ ] `L2` How are consumer offsets stored and committed?
- [ ] `L2` How is each partition replicated, and when is a write acknowledged?
- [ ] `L2` How do consumer groups divide partitions? What triggers a rebalance?
- [ ] `L2` How does a producer pick a partition, and how are writes batched?
- [ ] `L3` How do you elect a new partition leader without losing committed data? ↳ ISR, high watermark, leader epoch, controller
- [ ] `L3` How would you add delayed messages or priorities to this design?
- [ ] `L3` How do you make retention cheap for months of data? ↳ segment files, tiered storage to object store
- [ ] `L3` How would you give exactly-once from producer to consumer in your design?

## 29.30 API gateway
**Learn:** https://microservices.io/patterns/apigateway.html · https://konghq.com/learning-center/api-gateway · https://www.envoyproxy.io/docs/envoy/latest/intro/what_is_envoy
### Opening
- [ ] `L2` Design an API gateway for 200 internal services.
### Clarify
- [ ] `L2` What do you clarify for the API gateway? ↳ protocols (REST/gRPC/WebSocket), auth types, rate limits, latency budget, multi-tenant
### Estimate
- [ ] `L2` 500k RPS with a 5 ms added-latency budget. How many gateway instances, and what can't you do inline?
### Deep dives
- [ ] `L2` What does the request pipeline look like? ↳ TLS, auth, rate limit, route, transform, proxy, log
- [ ] `L2` How do routing rules and config get updated without restarts?
- [ ] `L2` How do you validate JWTs without calling the auth service each time? ↳ cached JWKS, signature check locally
- [ ] `L2` How does the gateway proxy WebSockets and streaming (SSE) responses?
- [ ] `L2` What does the gateway log and trace for every request?
- [ ] `L3` How do you avoid the gateway becoming a bottleneck and a single point of failure?
- [ ] `L3` What is request aggregation in a gateway and when does it become a mess?
- [ ] `L3` How do you do canary routing by header or percentage through the gateway?
- [ ] `L3` Build vs buy: Kong / Envoy / APIM / AWS API Gateway — how do you choose?
- [ ] `L3` How do you deploy a gateway config change safely when one bad rule could break every API?

## 29.31 Feature flag / remote config service
**Learn:** https://martinfowler.com/articles/feature-toggles.html · https://docs.getunleash.io/understanding-unleash/the-anatomy-of-unleash · https://launchdarkly.com/blog/ (architecture posts)
### Opening
- [ ] `L2` Design a feature flag service like LaunchDarkly.
### Clarify
- [ ] `L2` What do you clarify for the feature flag service? ↳ server and client SDKs, targeting rules, percentage rollouts, change propagation time, audit
### Estimate
- [ ] `L2` 1,000 services, 50k instances, flags read on every request. Why can't each read hit a central server?
### Deep dives
- [ ] `L2` Where is flag evaluation done — in the SDK or on the server? Trade-offs.
- [ ] `L2` How do flag changes reach SDKs quickly? ↳ streaming (SSE) + polling fallback, local cache
- [ ] `L2` How do you do a stable 10% rollout so a user doesn't flip between on and off? ↳ hash(user id + flag) mod 100
- [ ] `L2` What happens if the flag service is down?
- [ ] `L2` What is the data model for flags, rules, segments and environments?
- [ ] `L3` How do you evaluate flags in a mobile app without leaking all rules to the client?
- [ ] `L3` How do you keep an audit trail and roll back a bad flag change?
- [ ] `L3` How do you clean up stale flags in the codebase?
- [ ] `L3` How would you use flags to roll out a new LLM model or prompt at AiRA?
- [ ] `L3` How do you run A/B experiments on top of flags and get clean metrics?

## 29.32 Hiring platform candidate matching — tie to Jigsaw
**Learn:** https://www.linkedin.com/blog/engineering (search and matching posts) · HOL ch8 "Semantic Search" (pdf p247–280) · AIE ch6 "Retrieval Algorithms" (pdf p281–291)
### Opening
- [ ] `L2` Design a system that matches candidates to job openings and ranks them for recruiters.
### Clarify
- [ ] `L2` What do you clarify for candidate matching? ↳ number of jobs/candidates, structured vs free-text, hard filters, explainability, bias rules
### Estimate
- [ ] `L2` 10M candidate profiles, 100k open jobs, recruiters search 50k times a day. Index size and QPS?
### Deep dives
- [ ] `L2` How do you parse resumes and job descriptions into structured fields? ↳ LLM extraction + schema validation + human review
- [ ] `L2` Hard filters (location, years, visa) vs soft relevance: how do you combine them?
- [ ] `L2` Keyword search vs embeddings vs hybrid for matching skills.
- [ ] `L2` What does the two-stage pipeline look like? ↳ candidate retrieval (filters + ANN/BM25), then reranker
- [ ] `L2` How do you keep the index fresh when profiles change?
- [ ] `L2` How do you explain to a recruiter why a candidate ranked high?
- [ ] `L3` How do you evaluate match quality? ↳ recruiter actions as labels, offline ranking metrics, A/B tests
- [ ] `L3` How do you avoid biased ranking (gender, college) and prove it?
- [ ] `L3` Skill synonyms ("React" vs "ReactJS" vs "frontend"): how do you normalise them?
- [ ] `L3` How did matching work at Jigsaw, and what would you change with today's models?

## 29.33 Photo sharing (Instagram)
**Learn:** HelloInt breakdown "Instagram" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · https://instagram-engineering.com · DDIA ch1 (pdf p31–35)
### Opening
- [ ] `L2` Design Instagram: upload photos, follow people, see a feed, like and comment.
### Clarify
- [ ] `L2` What do you clarify for photo sharing? ↳ photos vs video vs stories, feed ranking, DAU, read:write ratio, global users
### Estimate
- [ ] `L2` 500M DAU, 100M photo uploads a day at 2 MB after compression. Storage per year and CDN egress?
### Deep dives
- [ ] `L2` Walk through the upload pipeline. ↳ presigned upload, resize to sizes, store variants, CDN, metadata write
- [ ] `L2` Why generate multiple image sizes at upload time instead of on request?
- [ ] `L2` How do you build the feed? Reuse your news-feed answer and say what changes for media.
- [ ] `L2` How do you count likes on a viral photo? ↳ sharded counters, async aggregation, approximate display
- [ ] `L2` Which databases store users, posts, follows and likes, and why?
- [ ] `L2` How would you build the explore / search page at a high level?
- [ ] `L3` How do you make images load fast on slow Indian mobile networks? ↳ WebP/AVIF, progressive, size per device, edge CDN
- [ ] `L3` How do you moderate uploads for unsafe content at upload scale?
- [ ] `L3` How do stories (24-hour expiry) change storage and feed design?
- [ ] `L3` A user deletes their account. How do you remove all their photos, including CDN copies?

## 29.34 Coupon and promo system
**Learn:** https://stripe.com/blog/idempotency · DDIA ch7 "Preventing Lost Updates" (pdf p255) · https://tech-blog.flipkart.net
### Opening
- [ ] `L2` Design a coupon / promo code system for an e-commerce site.
### Clarify
- [ ] `L2` What do you clarify for the coupon system? ↳ coupon types, per-user and global limits, stacking rules, expiry, targeting
### Estimate
- [ ] `L2` A coupon limited to the first 10,000 users goes viral on social media. Redemption QPS at launch?
### Deep dives
- [ ] `L2` How do you model coupons, rules and redemptions?
- [ ] `L2` How do you enforce "max 10,000 redemptions" under heavy concurrency? ↳ atomic counter (Redis DECR / conditional update), reserve then confirm
- [ ] `L2` How do you enforce "once per user" across devices and retries? ↳ unique (user, coupon) constraint, idempotency key
- [ ] `L2` When is a coupon "used" — at apply, at checkout, or at payment success? What if payment fails?
- [ ] `L2` What APIs do you expose: validate, apply, redeem, reverse?
- [ ] `L2` How do you cache coupon rules so validation at checkout stays fast?
- [ ] `L3` How do you detect coupon abuse (fake accounts, shared codes)?
- [ ] `L3` How do you evaluate stacking rules fast for a cart with 30 items?
- [ ] `L3` How do you generate 1M unique, unguessable single-use codes?
- [ ] `L3` How do you reconcile redemptions against orders and refunds at day end?

## 29.35 Online judge / code execution sandbox
**Learn:** HelloInt breakdown "LeetCode" (https://www.hellointerview.com/learn/system-design/problem-breakdowns/overview) · https://gvisor.dev/docs/ · https://firecracker-microvm.github.io
### Opening
- [ ] `L2` Design LeetCode's "run code" backend.
- [ ] `L2` Design a sandbox that runs untrusted code from 1,000 users at once.
### Clarify
- [ ] `L2` What do you clarify for the online judge? ↳ languages, time/memory limits, contest peaks, network access, result latency
### Estimate
- [ ] `L2` A contest with 50k users submitting every 2 minutes, 5 s per run. How many concurrent sandboxes?
### Deep dives
- [ ] `L2` Why put submissions on a queue instead of running them in the API request?
- [ ] `L2` How do you isolate untrusted code? ↳ containers + seccomp, gVisor, Firecracker microVMs; no network, read-only FS
- [ ] `L2` How do you enforce CPU time, wall time and memory limits?
- [ ] `L2` How does the user get the result? ↳ poll job status, or WebSocket/SSE push
- [ ] `L2` How do you compare outputs (exact, whitespace, floating point, custom checkers)?
- [ ] `L3` Container vs microVM vs WASM sandbox: security and cold-start trade-offs.
- [ ] `L3` How do you keep warm sandbox pools so cold starts don't kill latency?
- [ ] `L3` How do you stop fork bombs, crypto miners and sandbox escapes?
- [ ] `L3` What from this design did you reuse for AiRA's browser agent sandboxes?
- [ ] `L3` How do you handle a contest spike and keep the contest leaderboard live?

## 29.36 Search engine over documents
**Learn:** DDIA ch3 "Full-text search and fuzzy indexes" (pdf p104) · https://www.elastic.co/blog/found-elasticsearch-from-the-bottom-up · *Introduction to Information Retrieval* (Manning) ch1–2
### Opening
- [ ] `L2` Design search over 1 billion documents (a site search or internal company search).
### Clarify
- [ ] `L2` What do you clarify for document search? ↳ document types, update rate, query latency, ranking signals, permissions, languages
### Estimate
- [ ] `L2` 1B docs at 10 KB of text. Raw size, index size, and number of shards?
### Deep dives
- [ ] `L2` Ingest path: crawl/ingest, parse, tokenise, index. Where do queues sit?
- [ ] `L2` Shard by document or by term? Why does almost everyone shard by document?
- [ ] `L2` How does a query fan out to shards and merge top-k results?
- [ ] `L2` How do you rank: BM25, freshness, popularity, personalisation?
- [ ] `L2` How do you apply updates and deletes to the index in near real time?
- [ ] `L2` How do replicas help query throughput and failover in the search cluster?
- [ ] `L3` How do you enforce per-user document permissions in search results without slowing queries?
- [ ] `L3` How do you add semantic (vector) search alongside keyword search?
- [ ] `L3` How do you measure search quality? ↳ click-through, NDCG on judged queries, zero-result rate
- [ ] `L3` How do you answer a query whose common term matches 100M documents quickly? ↳ early termination, tiered index, result caching

## 29.37 Expense splitting (Splitwise)
**Learn:** https://www.geeksforgeeks.org/minimize-cash-flow-among-given-set-friends-borrowed-money/ · *System Design Interview* (Xu) vol2 ch12 "Digital Wallet" (ledger ideas)
### Opening
- [ ] `L2` Design the backend for Splitwise.
### Clarify
- [ ] `L2` What do you clarify for expense splitting? ↳ groups, split types, currencies, settlements, offline edits, notifications
### Estimate
- [ ] `L2` 20M users, 5 expenses a week each. Why is scale easy here and correctness the real problem?
### Deep dives
- [ ] `L2` Store expenses and compute balances, or store balances directly? Trade-offs.
- [ ] `L2` How do you compute "who owes whom" in a group?
- [ ] `L2` How do you simplify debts to the fewest payments? ↳ net balances, greedy match max creditor/debtor
- [ ] `L2` How do you handle editing or deleting an old expense?
- [ ] `L2` What APIs and tables do you need (users, groups, expenses, splits, settlements)?
- [ ] `L2` How do you record a settlement payment — is it just another expense?
- [ ] `L3` Two members edit the same expense at once. How do you avoid lost updates?
- [ ] `L3` How do you handle multi-currency groups and exchange rates over time?
- [ ] `L3` How do you notify group members of new expenses without spamming them?
- [ ] `L3` How would you settle up through real UPI payments and keep both records consistent?

## 29.38 Calendar and meeting scheduler (Google Calendar)
**Learn:** https://datatracker.ietf.org/doc/html/rfc5545 (iCalendar RRULE) · DDIA ch8 "Unreliable Clocks" (pdf p300)
### Opening
- [ ] `L2` Design Google Calendar with meeting invites and free/busy lookup.
### Clarify
- [ ] `L2` What do you clarify for the calendar? ↳ recurrence, time zones, invites across orgs, rooms, reminders, sync with other clients
### Estimate
- [ ] `L2` 100M users, 5 events/day, reminders on most. Reminder fires per second at the 9 am peak?
### Deep dives
- [ ] `L2` How do you store recurring events? Expand all instances or store the rule? ↳ store RRULE + exceptions; expand on read for a window
- [ ] `L2` How do you store times so DST changes don't break meetings? ↳ wall time + IANA zone for future events, UTC for instants
- [ ] `L2` How do you find a free slot for 8 people? ↳ free/busy intervals, merge, intersect
- [ ] `L2` How do invites and RSVPs flow between users and organisations?
- [ ] `L2` How do you send event reminders reliably at the right time?
- [ ] `L2` How do you sync events with phones and other clients (CalDAV, push changes)?
- [ ] `L3` "Edit this and following events" on a recurring series: how do you model it?
- [ ] `L3` How do you prevent double-booking a meeting room?
- [ ] `L3` How would AiRA's reminder engine plug into a calendar like this?
- [ ] `L3` How do you partition calendar data and answer free/busy across many users fast?

## 29.39 ChatGPT-like chat service with streaming
**Learn:** AIE ch9 "Inference Optimization" (pdf p429–472, latency metrics p436) · AIE ch10 (pdf p473–518) · LEH ch10 "Deploying LLMs" (pdf p384–429) · https://huyenchip.com/2024/07/25/genai-platform.html · https://docs.vllm.ai
### Opening
- [ ] `L2` Design ChatGPT: users chat with an LLM and see tokens stream in.
### Clarify
- [ ] `L2` What do you clarify for the ChatGPT-like chat service? ↳ own GPUs or API, users, context length, history retention, files/tools, free vs paid tiers
- [ ] `L2` Which latency numbers matter for chat? ↳ time to first token, tokens per second, end-to-end
### Estimate
- [ ] `L2` 10M DAU, 15 messages each, 500 output tokens per reply. Tokens per second at peak, and GPUs needed?
- [ ] `L2` What is the monthly API cost of that traffic at $X per million tokens?
### Deep dives
- [ ] `L2` How do tokens stream from the model to the browser? ↳ model stream → server → SSE/WebSocket → client
- [ ] `L2` SSE vs WebSocket for token streaming: which and why?
- [ ] `L2` How do you store conversations and messages? Which DB and partition key?
- [ ] `L2` The conversation exceeds the context window. What do you do? ↳ truncate, summarise older turns, retrieve relevant past turns
- [ ] `L2` The user refreshes the page mid-stream. How do they get the rest of the answer? ↳ generation continues server-side, buffer in Redis Streams, resume by offset
- [ ] `L2` The user clicks "Stop generating". What happens server-side?
- [ ] `L2` How do you rate-limit and meter usage per user and tier? ↳ tokens per minute, monthly quotas, priority queues
- [ ] `L2` How do you handle file uploads and tool calls (web search, code) in a chat?
- [ ] `L3` How does LLM serving batch requests? What is continuous batching and KV cache? ↳ vLLM, PagedAttention, iteration-level scheduling
- [ ] `L3` How do you route requests across GPU pools and models with different costs?
- [ ] `L3` How does prefix/prompt caching cut cost and latency for long system prompts?
- [ ] `L3` Provider is down or slow. How do you fail over across providers mid-conversation?
- [ ] `L3` How do you autoscale GPU inference when cold start takes minutes?
- [ ] `L3` How do you add moderation/guardrails on input and output without killing latency?
- [ ] `L3` How do you collect feedback (thumbs up/down) and use it?
- [ ] `L3` How did AiRA stream LLM output (SSE → Redis Streams → WebSocket), and why that chain?

## 29.40 Realtime voice assistant — tie to AiRA
**Learn:** https://docs.livekit.io/agents/ · https://platform.openai.com/docs/guides/realtime · https://developers.deepgram.com/docs/streaming · AIE ch9 "Latency metrics" (pdf p436) · DDIA ch4 "Message-Passing Dataflow" (pdf p154)
### Opening
- [ ] `L2` Design a realtime voice assistant: the user talks, the assistant answers out loud with low latency.
### Clarify
- [ ] `L2` What do you clarify for the realtime voice assistant? ↳ latency target, languages, interruptions, tools/actions, devices, concurrent calls, telephony
- [ ] `L2` Cascaded STT → LLM → TTS vs a speech-to-speech model: what do you ask to decide?
### Estimate
- [ ] `L2` Build a latency budget from end of user speech to first audio out. ↳ VAD end ~200ms, STT final, LLM TTFT, TTS first chunk, network
- [ ] `L2` 10k concurrent calls at 16 kHz 16-bit audio: bandwidth in and out, and WebSocket servers needed?
### Deep dives
- [ ] `L2` Draw the voice pipeline. ↳ mic, WebSocket, VAD, streaming STT, LLM, streaming TTS, client playback
- [ ] `L2` What is VAD and how do you detect the user has finished speaking (endpointing)?
- [ ] `L2` What is barge-in, and what must happen in every stage when the user interrupts? ↳ stop TTS playback, cancel LLM/TTS, truncate history to heard audio
- [ ] `L2` Why stream every stage instead of waiting for each to finish?
- [ ] `L2` How do you chunk LLM output for TTS so speech starts early but sounds natural? ↳ sentence/phrase boundaries
- [ ] `L2` WebSockets vs WebRTC for the audio transport: trade-offs on mobile networks.
- [ ] `L2` How do you handle tool calls (calendar, reminders) mid-conversation without dead air? ↳ filler speech, parallel tool calls, timeouts
- [ ] `L2` Which audio formats and codecs do you send over the wire, and why?
- [ ] `L3` Where are buffers in the pipeline, and how do you apply backpressure without adding latency?
- [ ] `L3` How do you scale voice sessions horizontally when each session is stateful? ↳ sticky session per call, session state in Redis for recovery
- [ ] `L3` STT or TTS vendor degrades mid-call. How do you fail over?
- [ ] `L3` How do you measure p50/p95 voice-to-voice latency in production?
- [ ] `L3` How do you handle echo, background noise and the assistant hearing itself?
- [ ] `L3` What did AiRA's voice architecture look like, what was the hardest latency bug, and how did you fix it?
- [ ] `L3` How do you store call audio and transcripts with privacy and consent?
- [ ] `L3` How would you cut per-minute cost of a voice call by half?

## 29.41 RAG over a company's documents at scale
**Learn:** AIE ch6 "RAG" (pdf p277), "Retrieval Algorithms" (pdf p281–291) · HOL ch8 (pdf p247–280, RAG p271) · LEH ch9 "RAG inference pipeline" (pdf p346) · https://eugeneyan.com/writing/llm-patterns/ · https://qdrant.tech/documentation/concepts/
### Opening
- [ ] `L2` Design a RAG chatbot over a company's documents.
- [ ] `L2` Design a RAG system for 10M documents with per-user permissions.
### Clarify
- [ ] `L2` What do you clarify for the RAG system? ↳ sources (Drive, Confluence, Slack), size, update rate, permissions, citations, languages, accuracy bar
### Estimate
- [ ] `L2` 10M docs, 20 chunks each, 1,024-dim float32 vectors. Vector index memory, and with quantisation?
- [ ] `L2` Embedding cost and time for the initial backfill of 200M chunks?
### Deep dives
- [ ] `L2` Draw the RAG ingestion pipeline. ↳ connectors, parse, clean, chunk, embed, upsert with metadata + ACLs
- [ ] `L2` How do you chunk documents? Fixed size vs structure-aware vs semantic chunking.
- [ ] `L2` Draw the RAG query pipeline. ↳ rewrite query, hybrid retrieve, filter by ACL, rerank, build prompt, generate with citations
- [ ] `L2` Why hybrid retrieval (BM25 + vectors)? How do you fuse the scores? ↳ reciprocal rank fusion
- [ ] `L2` What does a reranker add, and what does it cost?
- [ ] `L2` How do you enforce per-document permissions so retrieval never leaks? ↳ ACL metadata filter at query time, synced from source
- [ ] `L2` How do you keep the index fresh when documents are edited or deleted?
- [ ] `L2` How do you make the model cite sources and refuse when the answer is not in the docs?
- [ ] `L3` How do you evaluate retrieval and answer quality separately? ↳ recall@k, MRR on labelled set; faithfulness, answer relevance
- [ ] `L3` Users complain answers are wrong. Walk through how you debug: retrieval, ranking or generation?
- [ ] `L3` How do you handle tables, PDFs with images and scanned documents?
- [ ] `L3` Multi-tenant RAG: one collection with tenant filter vs collection per tenant in Qdrant?
- [ ] `L3` You switch to a new embedding model. How do you re-embed 200M chunks with no downtime? ↳ dual index, backfill, shadow eval, alias swap
- [ ] `L3` When is long-context stuffing better than RAG?
- [ ] `L3` How do you handle questions that need many documents (aggregation) rather than one passage?

## 29.42 Multi-tenant LLM gateway
**Learn:** AIE ch10 "Router and Gateway" (pdf p480), "Caching" (pdf p484) · https://docs.litellm.ai · https://huyenchip.com/2024/07/25/genai-platform.html
### Opening
- [ ] `L2` Design an LLM gateway that all product teams and tenants use to call models.
### Clarify
- [ ] `L2` What do you clarify for the multi-tenant LLM gateway? ↳ providers, streaming, tenants, budgets, data residency, logging rules, latency overhead allowed
### Estimate
- [ ] `L2` 5k requests/s, 30% streaming, average 2k tokens each. Gateway instances and log storage per day?
### Deep dives
- [ ] `L2` What features does the gateway own? ↳ unified API, auth, routing, fallbacks, retries, rate limits, metering, logging, caching
- [ ] `L2` How do you abstract different providers' APIs (OpenAI, Anthropic, Gemini) behind one interface?
- [ ] `L2` How do you route by cost, latency or capability?
- [ ] `L2` How do fallbacks work when a provider returns 429 or 5xx — including mid-stream?
- [ ] `L2` How do you rate-limit and budget per tenant in tokens and money?
- [ ] `L2` How do you count tokens and bill tenants accurately for streamed responses?
- [ ] `L2` Exact cache vs semantic cache: when is each safe?
- [ ] `L3` How do you keep tenant data isolated in logs, caches and provider calls? ↳ tenant-scoped cache keys, PII redaction, per-tenant retention, no-train flags
- [ ] `L3` How do you add guardrails (PII, prompt injection, output filters) without adding much latency?
- [ ] `L3` How do you keep the gateway from becoming a single point of failure for the whole company?
- [ ] `L3` How do you roll out a new model version to 5% of traffic and compare quality?

## 29.43 Agent platform that runs browser tasks for users — tie to AiRA
**Learn:** https://www.anthropic.com/engineering/building-effective-agents · AIE ch6 "Agents" (pdf p299) · AIE ch10 "Agent patterns" (pdf p487) · https://playwright.dev/docs/intro · https://firecracker-microvm.github.io
### Opening
- [ ] `L2` Design a platform where an AI agent controls a browser to do tasks for users (book, fill forms, research).
### Clarify
- [ ] `L2` What do you clarify for the browser agent platform? ↳ task length, concurrency, sites, logins/secrets, human approval points, cost per task
### Estimate
- [ ] `L2` 2,000 concurrent browser sessions at ~1 GB RAM each. How many machines, and cost per task-minute?
### Deep dives
- [ ] `L2` Draw the components. ↳ task API, queue, orchestrator/agent loop, browser pool, sandbox, state store, live view
- [ ] `L2` How does the agent loop work? ↳ observe (DOM/screenshot), plan, act (tool), check, repeat; step limits
- [ ] `L2` How do you isolate each user's browser session? ↳ container/microVM per session, separate profiles, network egress rules
- [ ] `L2` How do you manage a warm pool of browsers to avoid cold starts?
- [ ] `L2` How do you persist task state so a crash mid-task can resume?
- [ ] `L2` How do users watch the agent live and take over? ↳ CDP screencast / VNC stream over WebSocket
- [ ] `L3` How do you handle user credentials and sessions without the model ever seeing passwords?
- [ ] `L3` How do you defend against prompt injection from web pages the agent reads?
- [ ] `L3` Which actions need human approval, and how do you pause and resume the task?
- [ ] `L3` How do you handle CAPTCHAs and bot blocks — and where do you draw the line?
- [ ] `L3` How do you measure task success rate and debug failed runs? ↳ step traces, screenshots, replay
- [ ] `L3` What did AiRA's browser agent sandbox look like, and what limited concurrency?

## 29.44 Customer-support agent that takes actions
**Learn:** https://www.anthropic.com/engineering/building-effective-agents · AIE ch10 "Guardrails" (pdf p475), "User feedback" (pdf p498)
### Opening
- [ ] `L2` Design a customer-support AI agent that can issue refunds and change orders.
### Clarify
- [ ] `L2` What do you clarify for the customer-support agent? ↳ allowed actions, money limits, escalation rules, channels, languages, audit needs
### Estimate
- [ ] `L2` 50k tickets a day, 6 LLM calls per ticket. Token cost per ticket and per month?
### Deep dives
- [ ] `L2` How do you expose actions to the model as tools with permissions? ↳ narrow tools, server-side auth checks, limits per action
- [ ] `L2` Which actions need human approval, and how does the approval flow work?
- [ ] `L2` How do you hand off to a human agent with full context?
- [ ] `L2` What goes in the audit log for every action?
- [ ] `L2` How does the agent fetch order history and policy context (APIs + RAG over policies)?
- [ ] `L2` How do you keep conversation state across channels (chat, email, phone)?
- [ ] `L3` How do you stop a user talking the agent into a refund it shouldn't give?
- [ ] `L3` How do you make tool calls idempotent so a retried step doesn't refund twice?
- [ ] `L3` How do you evaluate the agent before letting it act on real customers? ↳ replay past tickets, sandbox tools, shadow mode
- [ ] `L3` What do you monitor live for this agent? ↳ resolution rate, escalation rate, refund totals, CSAT, anomalies

## 29.45 Email / ticket triage pipeline
**Learn:** AIE ch10 (pdf p473–518) · https://eugeneyan.com/writing/llm-patterns/ · DDIA ch11 (streams)
### Opening
- [ ] `L2` Design a pipeline that classifies incoming emails/tickets, extracts fields and routes them.
### Clarify
- [ ] `L2` What do you clarify for the triage pipeline? ↳ volume, categories, latency (realtime or batch), accuracy bar, human review, languages
### Estimate
- [ ] `L2` 1M emails a day. LLM cost with a large model vs a small classifier first?
### Deep dives
- [ ] `L2` Draw the triage pipeline. ↳ ingest → queue → classify → extract → validate → route; low-confidence → human queue
- [ ] `L2` Small model / rules first, LLM only for hard cases: how do you build that cascade?
- [ ] `L2` How do you get structured output reliably? ↳ JSON schema / function calling, validation, retry on failure
- [ ] `L2` How do you use confidence to decide what goes to humans?
- [ ] `L2` How do you handle attachments and quoted email threads before classification?
- [ ] `L2` How do you keep the pipeline flowing when the LLM provider rate-limits you?
- [ ] `L3` How do human corrections flow back to improve the system?
- [ ] `L3` How do you detect drift when new kinds of tickets appear?
- [ ] `L3` How do you measure precision and recall per category, and which errors cost most?
- [ ] `L3` How do you redact PII before sending emails to a third-party LLM?

## 29.46 Document extraction at scale — tie to Jigsaw job extraction
**Learn:** AIE ch9 "Batching" (pdf p464) · https://platform.openai.com/docs/guides/batch · https://docs.anthropic.com/en/docs/build-with-claude/batch-processing
### Opening
- [ ] `L2` Design a system that extracts structured data from millions of documents (job posts, resumes, invoices) with LLMs.
### Clarify
- [ ] `L2` What do you clarify for document extraction? ↳ document formats, schema, accuracy target, deadline (realtime or overnight), budget
### Estimate
- [ ] `L2` 5M documents at 3k input tokens each. Cost with realtime API vs batch API, and time to finish?
### Deep dives
- [ ] `L2` How do you parse PDFs, HTML and scanned images before the LLM?
- [ ] `L2` How do you split work into jobs, track status and retry failures?
- [ ] `L2` How do you stay under provider rate limits with many workers? ↳ token-bucket per provider, shared limiter, adaptive concurrency
- [ ] `L2` How do you validate outputs against the schema and fix bad ones?
- [ ] `L2` What does the data model for documents, jobs, attempts and results look like?
- [ ] `L2` How do you choose a model per document type by cost and accuracy?
- [ ] `L3` How do you measure extraction accuracy without labelling everything? ↳ golden set, sampling audits, field-level metrics
- [ ] `L3` How do you re-run only changed or failed documents when the prompt changes?
- [ ] `L3` How did Jigsaw's job extraction work, and how would you make it 10× cheaper?
- [ ] `L3` How do you handle documents longer than the context window?

## 29.47 Semantic search and recommendations with embeddings
**Learn:** HOL ch8 "Semantic Search" (pdf p247–280) · HOL ch2 "Text Embeddings" (pdf p83) · https://www.pinecone.io/learn/series/faiss/hnsw/ · https://eugeneyan.com/writing/system-design-for-discovery/
### Opening
- [ ] `L2` Design semantic search and "similar items" recommendations for a catalogue of 50M items.
### Clarify
- [ ] `L2` What do you clarify for semantic search and recommendations? ↳ item types, filters, personalisation, freshness, latency, cold-start items and users
### Estimate
- [ ] `L2` 50M items × 768-dim vectors. Memory for HNSW in float32 vs int8, and QPS per node?
### Deep dives
- [ ] `L2` What does the two-stage retrieval + ranking architecture look like?
- [ ] `L2` How do you build item and user embeddings?
- [ ] `L2` HNSW vs IVF vs flat search: trade-offs in recall, memory and build time.
- [ ] `L2` How do you combine vector search with filters (price, category, in stock)? ↳ pre-filter vs post-filter vs filtered HNSW (Qdrant payload index)
- [ ] `L2` How do you handle new items with no interactions (cold start)?
- [ ] `L2` How do you serve "similar items" fast — precompute or query on the fly?
- [ ] `L3` How do you evaluate recommendations offline and online? ↳ recall@k, NDCG; A/B test CTR, conversion
- [ ] `L3` How do you avoid feedback loops where popular items get more popular?
- [ ] `L3` How do you update embeddings for 50M items without a full rebuild?
- [ ] `L3` How do you blend business rules (sponsored, in stock, diversity) into the final ranking?

## 29.48 LLM evaluation platform
**Learn:** AIE ch3 "Evaluation Methodology", ch4 "Evaluate AI Systems" · AIE ch10 "Monitoring and Observability" (pdf p489) · LEH ch11 "LLMOps" (pdf p430) · https://hamel.dev/blog/posts/evals/
### Opening
- [ ] `L2` Design a platform to evaluate LLM features before release and monitor them in production.
- [ ] `L2` How do you evaluate and monitor an LLM system in production?
### Clarify
- [ ] `L2` What do you clarify for the LLM evaluation platform? ↳ teams/use cases, metrics, human labels, CI integration, cost limits, data privacy
### Estimate
- [ ] `L2` 50 eval suites × 1,000 cases × 3 judge calls, run on every PR. Cost and time per run?
### Deep dives
- [ ] `L2` What are the core objects? ↳ datasets, test cases, prompts/versions, runs, scores, judges, reports
- [ ] `L2` Exact match vs heuristic vs LLM-as-judge vs human review: when each?
- [ ] `L2` How do you make LLM-as-judge reliable? ↳ clear rubric, calibrate vs human labels, pairwise, position-bias checks
- [ ] `L2` How do you run evals in CI and block a bad prompt change?
- [ ] `L2` How do you sample production traffic into eval datasets safely?
- [ ] `L2` How do you version prompts, models and datasets so a run is reproducible?
- [ ] `L3` How do you evaluate multi-step agents, not just single responses?
- [ ] `L3` Scores are noisy between runs. How do you tell a real regression from noise?
- [ ] `L3` How did you evaluate AiRA's agent or memory quality, and what would you build now?
- [ ] `L3` How do you turn user feedback and production failures into new test cases automatically?

## 29.49 Long-term memory service for an assistant — tie to AiRA
**Learn:** https://arxiv.org/abs/2310.08560 (MemGPT) · https://docs.mem0.ai · https://memgraph.com/docs · https://qdrant.tech/documentation/concepts/ · AIE ch6 (pdf p277–299)
### Opening
- [ ] `L2` Design a long-term memory service so an assistant remembers users across conversations.
### Clarify
- [ ] `L2` What do you clarify for the memory service? ↳ what counts as memory, retention, user control/deletion, latency budget, users, privacy
### Estimate
- [ ] `L2` 1M users, 50 new memories each a month, 1,536-dim vectors. Storage after a year? Retrieval QPS?
### Deep dives
- [ ] `L2` What do you store: raw transcripts, extracted facts, summaries, a graph? Why?
- [ ] `L2` How do you extract memories from a conversation? Sync or async? ↳ async LLM extraction after turn/session, so chat latency isn't hit
- [ ] `L2` How do you retrieve relevant memories for a new message within the latency budget?
- [ ] `L2` Vector store vs graph store vs both: what does each answer well? ↳ vectors: fuzzy similarity; graph: entities, relations, multi-hop
- [ ] `L2` How do you update or contradict an old memory ("I moved to Pune")?
- [ ] `L2` How does the user see, edit and delete what the assistant remembers?
- [ ] `L3` How do you keep Memgraph and Qdrant consistent when one write fails?
- [ ] `L3` How do you stop memory from filling the prompt with stale or irrelevant facts? ↳ recency/importance scoring, decay, summarisation, top-k budget
- [ ] `L3` How do you evaluate whether memory makes answers better?
- [ ] `L3` How do you isolate users' memories and handle "forget me" requests across all stores?
- [ ] `L3` What did AiRA's memory design get right, and what would you redesign?

## 29.50 Long-running generation job service (text-to-video / long reports)
**Learn:** AIE ch9 (pdf p429–472) · LEH ch10 "Autoscaling" (pdf p384–429) · https://docs.temporal.io/
### Opening
- [ ] `L2` Design a service where users submit long generation jobs (text-to-video, long reports) that take minutes.
### Clarify
- [ ] `L2` What do you clarify for the long-running job service? ↳ job duration, GPU or API, progress updates, cancellation, priority tiers, cost per job
### Estimate
- [ ] `L2` 100k jobs a day at 3 GPU-minutes each. GPUs needed at peak with a 2× peak factor?
### Deep dives
- [ ] `L2` Why an async job API (submit → job id → status) instead of a long HTTP request?
- [ ] `L2` What is the job state machine, and where is it stored?
- [ ] `L2` How do you stream progress and partial results to the user?
- [ ] `L2` How do you schedule jobs across GPU workers with priorities and fairness per user?
- [ ] `L2` How does a user cancel a job, and what happens to GPU work already running?
- [ ] `L2` Where are outputs stored and how are they delivered? ↳ blob storage, signed URL, notification
- [ ] `L3` A worker dies at 80% of a 10-minute job. How do you checkpoint and resume?
- [ ] `L3` How do you cap cost per user and stop runaway jobs?
- [ ] `L3` What did you learn building Lumen's job flow, and what would you change?
- [ ] `L3` How do you estimate queue wait time and show it honestly to users?

## 29.51 Rapid-fire round
- [ ] `L1` Base62 with 7 characters gives roughly how many codes?
- [ ] `L1` Fan-out on write or on read for a celebrity?
- [ ] `L1` Which Redis type powers a leaderboard?
- [ ] `L1` Which Redis type stores driver locations for nearby search?
- [ ] `L1` What are the Snowflake ID parts?
- [ ] `L1` Why presigned URLs for uploads?
- [ ] `L1` HLS / DASH are used for what?
- [ ] `L1` What prevents two users booking the same seat?
- [ ] `L1` What is a double-entry ledger?
- [ ] `L1` Why integers for money?
- [ ] `L1` OT or CRDT: which needs a central server?
- [ ] `L1` What does a URL frontier hold?
- [ ] `L1` How does a crawler check "already seen" cheaply?
- [ ] `L1` Where do you put the trie for autocomplete?
- [ ] `L1` What is a virtual waiting room?
- [ ] `L1` What does a heartbeat do for presence?
- [ ] `L1` What is a delivery receipt in chat?
- [ ] `L1` What is time to first token?
- [ ] `L1` What is barge-in?
- [ ] `L1` What is VAD?
- [ ] `L1` Why rerank after vector retrieval?
- [ ] `L1` Where must per-document permissions be enforced in RAG?
- [ ] `L1` What is semantic caching?
- [ ] `L1` What does an LLM gateway meter?
- [ ] `L1` Why sandbox each browser agent session?
- [ ] `L1` What is LLM-as-judge?
- [ ] `L1` Batch API vs realtime API: what do you trade?
- [ ] `L1` Async job API: what three endpoints?
