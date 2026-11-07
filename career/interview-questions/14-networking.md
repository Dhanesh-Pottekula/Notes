# 14. Networking fundamentals

Networking shows up in every backend loop: "what happens when you type a URL", TCP vs UDP, TLS, HTTP versions, and
"the service is timing out — debug it". A 3-year engineer must explain each layer a request crosses, read `curl -v`
and `ss` output, and reason about timeouts, retries and long-lived connections (your AiRA voice WebSocket is the
best story here). Syllabus: 2F Networking (`../../syllabus.html`).

## 14.1 Layers, and what happens when you type a URL
**Learn:** https://github.com/alex/what-happens-when · MDN "How the web works" (developer.mozilla.org) · *High Performance Browser Networking* (hpbn.co) ch.1–4 · ByteByteGo "What Happens When You Type a URL Into Your Browser?" (YouTube)
- [ ] `L1` Name the layers of the OSI model and of the TCP/IP model. Which ones matter in daily backend work?
- [ ] `L1` At which layer do IP, TCP, UDP, TLS, HTTP, DNS and Ethernet sit?
- [ ] `L1` What is a port? Why do we need ports on top of IP addresses?
- [ ] `L1` What is a socket? What 5 things identify a TCP connection? ↳ 5-tuple: protocol, src IP, src port, dst IP, dst port
- [ ] `L1` What happens when you type google.com and press Enter? Give the short version.
- [ ] `L1` What is a packet, a segment, a datagram and a frame?
- [ ] `L2` Now the deep version: walk me from the keypress to pixels, naming every lookup and handshake. ↳ cache/HSTS, DNS, TCP, TLS+ALPN, HTTP, server, render, keep-alive
- [ ] `L2` Before any network call, which local caches does the browser and OS check for the name? ↳ browser DNS cache, OS cache, `/etc/hosts`, HSTS preload list
- [ ] `L2` How many round trips does it take before the first byte of the response on a cold HTTPS/1.1 connection? On TLS 1.3? On HTTP/3?
- [ ] `L2` What is encapsulation? Show how an HTTP request is wrapped as it goes down the stack.
- [ ] `L2` How does your laptop find the MAC address of the router? ↳ ARP for the default gateway's IP
- [ ] `L2` What does the default gateway do? What is a routing table?
- [ ] `L2` What happens on the server side once the SYN arrives, up to your FastAPI handler running? ↳ kernel accept queue, accept(), event loop, worker, ASGI app
- [ ] `L2` Where in this path can a CDN, a load balancer and a reverse proxy sit?
- [ ] `L3` What is HSTS and how does it change the first request to a site?
- [ ] `L3` What is TCP Fast Open and why is it rarely used?
- [ ] `L3` How does the browser decide to use HTTP/2 or HTTP/3 for a site? ↳ ALPN in TLS; Alt-Svc header / HTTPS DNS record for h3
- [ ] `L3` A user in India hits your API hosted in us-east. Estimate the time to first byte and name what you would do about it.
- [ ] `L3` Which steps of the URL journey can be skipped on the second visit, and why? ↳ DNS cache, connection reuse, TLS resumption, HTTP cache

## 14.2 IP, subnets, CIDR, NAT and routing
**Learn:** https://www.cloudflare.com/learning/network-layer/what-is-a-subnet/ · AWS VPC docs "How Amazon VPC works" + "NAT gateways" (docs.aws.amazon.com/vpc) · Microsoft Learn "Azure Virtual Network overview" · Julia Evans "Bite Size Networking" (wizardzines.com)
- [ ] `L1` IPv4 vs IPv6: sizes and why IPv6 exists.
- [ ] `L1` What is a subnet? What does `/24` mean in `10.0.1.0/24`? ↳ first 24 bits are network; 256 addresses
- [ ] `L1` What are the private IPv4 ranges? ↳ 10/8, 172.16/12, 192.168/16
- [ ] `L1` What are `127.0.0.1` and `0.0.0.0`? What does binding a server to each mean?
- [ ] `L1` What is NAT? Why does almost every home and cloud network use it?
- [ ] `L1` Public IP vs private IP: which one does your VM in Azure/AWS have?
- [ ] `L2` How many usable hosts are in a `/26`? In a `/16`? Why does AWS give you 5 fewer per subnet?
- [ ] `L2` Your app works on your laptop but nobody can reach it in Docker or on the VM. You bound to `127.0.0.1`. Why does that matter?
- [ ] `L2` Public subnet vs private subnet in a VPC/VNet: what makes a subnet "public"? ↳ route to internet gateway; private uses NAT gateway for egress
- [ ] `L2` How does a VM in a private subnet download packages from the internet?
- [ ] `L2` SNAT vs DNAT vs port forwarding. Give an example of each.
- [ ] `L2` What is a security group vs a network ACL? Stateful vs stateless firewall. ↳ SG stateful per instance; NACL stateless per subnet
- [ ] `L2` What is ICMP and which tools use it? Why might ping fail while HTTP works?
- [ ] `L2` What is a VPC peering / VNet peering, and why can't the two networks have overlapping CIDRs?
- [ ] `L2` What is a bastion host, and what do you use instead today? ↳ SSM Session Manager, Azure Bastion, VPN/Tailscale
- [ ] `L2` Choose CIDR ranges for a VPC with 3 AZs, public and private subnets, and room to grow.
- [ ] `L3` What is MTU? What happens when a packet is bigger than the path MTU? ↳ fragmentation or ICMP "fragmentation needed"; PMTUD
- [ ] `L3` What is an MTU black hole and how does it show up? ↳ small requests work, large responses hang; ICMP blocked; MSS clamping
- [ ] `L3` Why do VPNs, VXLAN and overlay networks lower the effective MTU, and what breaks when nobody adjusts it?
- [ ] `L3` What is TCP MSS and how does it relate to MTU? ↳ MSS = MTU − IP − TCP headers, e.g. 1460
- [ ] `L3` How does NAT break inbound connections and peer-to-peer traffic? (sets up WebRTC)
- [ ] `L3` How many connections can one NAT gateway hold to the same destination, and why can it run out? ↳ ports per destination IP:port tuple; SNAT port exhaustion
- [ ] `L3` What is BGP, in one minute, and why do BGP mistakes take down big sites?
- [ ] `L3` What are private endpoints / PrivateLink and why use them for a managed Postgres or Redis?

## 14.3 TCP — connections, handshake, close and states
**Learn:** hpbn.co ch.2 "Building Blocks of TCP" · https://vincent.bernat.ch/en/blog/2014-tcp-time-wait-state-linux · RFC 9293 (TCP) · Hussein Nasser *Fundamentals of Backend Engineering* (TCP videos)
- [ ] `L1` What does TCP guarantee that IP does not? ↳ reliable, ordered, byte stream, flow and congestion control
- [ ] `L1` Walk me through the 3-way handshake.
- [ ] `L1` Why three steps and not two?
- [ ] `L1` Walk me through closing a TCP connection (the 4-way close).
- [ ] `L1` What is a sequence number? What is an ACK number?
- [ ] `L1` TCP is a byte stream, not a message stream. What does that mean for your application code? ↳ need framing: length prefix or delimiter; reads can split/merge
- [ ] `L2` What do SYN, ACK, FIN, RST and PSH flags mean?
- [ ] `L2` Why is the initial sequence number random?
- [ ] `L2` Name the TCP states a connection passes through on the client and on the server.
- [ ] `L2` What is TIME_WAIT? Which side ends up in it, and for how long? ↳ side that closes first; 2×MSL, 60 s on Linux
- [ ] `L2` Why does TIME_WAIT exist at all? ↳ late duplicate packets; final ACK may need resending
- [ ] `L2` What is CLOSE_WAIT? You see 5,000 sockets in CLOSE_WAIT on your server. What is the bug? ↳ peer closed; your app never called close(); leak
- [ ] `L2` Lots of TIME_WAIT on a server that calls an upstream API. Is it a problem? What do you do? ↳ connection reuse/pooling; not usually harmful
- [ ] `L2` What is a RST? When does the kernel send one? ↳ no listener on port, abort, data to closed socket, SO_LINGER 0
- [ ] `L2` "Connection refused" vs "connection timed out" vs "connection reset by peer": what does each tell you?
- [ ] `L2` What is a half-open connection? How can one side not know the other is gone?
- [ ] `L2` What is the listen backlog? What are the SYN queue and the accept queue?
- [ ] `L2` How does TCP retransmit lost data? What is RTO?
- [ ] `L2` What are duplicate ACKs and fast retransmit?
- [ ] `L2` What is SACK (selective acknowledgment)?
- [ ] `L3` What is a SYN flood and how do SYN cookies defend against it?
- [ ] `L3` What do `SO_REUSEADDR` and `SO_REUSEPORT` do? When do you need each?
- [ ] `L3` Why is `net.ipv4.tcp_tw_recycle` gone, and what is the safe `tcp_tw_reuse` alternative?
- [ ] `L3` What is a half-close (`shutdown(SHUT_WR)`), and which protocols rely on it?
- [ ] `L3` Accept queue overflows under load. What symptoms do clients see and which counters do you check? ↳ SYN drops, timeouts; `ss -lnt` Recv-Q, `netstat -s` overflows
- [ ] `L3` What is the C10K problem and how do epoll / kqueue solve it?
- [ ] `L3` What is a simultaneous open / simultaneous close, and does it happen in real life?

## 14.4 TCP performance — flow control, congestion control, Nagle, keepalive
**Learn:** hpbn.co ch.2 "Flow Control", "Slow-Start", "Congestion Avoidance", "Head-of-line blocking" · https://cloud.google.com/blog/products/networking/tcp-bbr-congestion-control-comes-to-gcp-your-internet-just-got-faster · DDIA ch8 "Timeouts and Unbounded Delays" (pdf p295–297)
- [ ] `L1` What is flow control? What is the receive window (rwnd)?
- [ ] `L1` What is congestion control? How is it different from flow control? ↳ protects network vs protects receiver
- [ ] `L1` What is slow start?
- [ ] `L1` What is head-of-line blocking in TCP?
- [ ] `L2` What is the congestion window (cwnd)? How do cwnd and rwnd together limit sending?
- [ ] `L2` What happens to cwnd when a packet is lost? Additive increase, multiplicative decrease.
- [ ] `L2` Why are new TCP connections slow for the first few round trips? What is the initial window today? ↳ slow start; IW10 ≈ 14 KB
- [ ] `L2` Why does reusing connections matter so much for latency? Tie it to slow start and handshakes.
- [ ] `L2` What is the bandwidth-delay product, and why does it set the window size you need?
- [ ] `L2` What is window scaling and why was it needed?
- [ ] `L2` What is a zero window? What does it tell you about the receiver?
- [ ] `L2` What is Nagle's algorithm? What problem did it solve?
- [ ] `L2` What is `TCP_NODELAY` and why do most realtime and RPC libraries turn it on?
- [ ] `L2` What is delayed ACK, and why do Nagle and delayed ACK together cause 40–200 ms stalls?
- [ ] `L2` What is TCP keepalive? Default timing on Linux? ↳ off by default; 2 hours idle, then 9 probes 75 s apart
- [ ] `L2` TCP keepalive vs HTTP keep-alive vs WebSocket ping/pong: three different things — explain each.
- [ ] `L2` Your WebSocket connections die after exactly 60 s idle behind a cloud load balancer. Why? ↳ LB idle timeout; send app-level pings below it
- [ ] `L2` Loss-based (Reno, CUBIC) vs model-based (BBR) congestion control.
- [ ] `L3` How does CUBIC grow its window, and why is it the Linux default?
- [ ] `L3` How does BBR estimate bottleneck bandwidth and min RTT? When does it beat CUBIC? ↳ lossy long-fat links; doesn't treat loss as congestion
- [ ] `L3` What is bufferbloat and how does it hurt realtime voice?
- [ ] `L3` What is ECN (explicit congestion notification)?
- [ ] `L3` What is TCP slow start after idle, and why might you disable it on long-lived connections?
- [ ] `L3` Ephemeral port exhaustion: what is it, when does a client hit it, and how do you fix it? ↳ many short outbound conns to one dst; pooling, range, more dst IPs
- [ ] `L3` What is the default ephemeral port range on Linux, and where do you see/change it? ↳ 32768–60999; `net.ipv4.ip_local_port_range`
- [ ] `L3` How many concurrent TCP connections can one server hold? What actually limits it? ↳ FDs, memory per socket, not the 65k port myth
- [ ] `L3` Which kernel settings would you look at for a server holding 200k idle WebSockets? ↳ ulimit nofile, somaxconn, tcp_mem, rmem/wmem, conntrack

## 14.5 UDP and when to use it
**Learn:** hpbn.co ch.3 "Building Blocks of UDP" · https://www.cloudflare.com/learning/ddos/glossary/user-datagram-protocol-udp/ · https://www.cloudflare.com/learning/performance/what-is-http3/
- [ ] `L1` What is UDP? What does it give up compared with TCP?
- [ ] `L1` Name four protocols that run on UDP. ↳ DNS, QUIC/HTTP3, RTP/WebRTC media, DHCP, NTP, syslog
- [ ] `L1` TCP vs UDP — which for a voice app, and why?
- [ ] `L1` Does UDP have connections or a handshake? Does it have ports?
- [ ] `L2` Why is UDP better for live voice and video even though packets can be lost? ↳ late packet is useless; no HOL blocking; codec hides loss
- [ ] `L2` What does an app built on UDP have to do itself? ↳ ordering, retransmit if needed, congestion control, framing, NAT keepalive
- [ ] `L2` What is a jitter buffer?
- [ ] `L2` How does a receiver notice lost UDP packets when there are no ACKs? ↳ app sequence numbers + timestamps (RTP), receiver reports
- [ ] `L2` What is the max UDP datagram size, and why keep payloads near 1,200 bytes? ↳ avoid IP fragmentation; QUIC/DNS stay under path MTU
- [ ] `L2` Why does DNS use UDP, and when does it fall back to TCP?
- [ ] `L2` Why can UDP be blocked or throttled on corporate networks, and what do realtime apps do then? ↳ fall back to TCP/TLS on 443 (TURN over TLS)
- [ ] `L2` Your AiRA voice runs over a WebSocket (TCP). What do you lose versus WebRTC over UDP, and why was it still the right call?
- [ ] `L3` What is a UDP amplification attack? Which protocols have been abused for it?
- [ ] `L3` Why did QUIC choose UDP instead of a new transport protocol? ↳ middleboxes/OS kernels ossified; userspace deployment
- [ ] `L3` How does NAT handle UDP when there is no connection? What is a NAT binding timeout?
- [ ] `L3` Design a simple reliable protocol over UDP. What do you need to add?

## 14.6 DNS
**Learn:** https://www.cloudflare.com/learning/dns/what-is-dns/ · https://www.cloudflare.com/learning/dns/dns-records/ · https://www.cloudflare.com/learning/cdn/glossary/time-to-live-ttl/ · Julia Evans "How DNS works" zine (wizardzines.com) · https://messwithdns.net
- [ ] `L1` What is DNS?
- [ ] `L1` Name the common record types and what each is for. ↳ A, AAAA, CNAME, MX, TXT, NS, SOA, SRV, CAA, PTR
- [ ] `L1` What is TTL in DNS?
- [ ] `L1` What is `/etc/hosts` and when does it win over DNS?
- [ ] `L2` Walk through a full resolution of `api.example.com` from a cold cache. ↳ stub → recursive resolver → root → .com TLD → authoritative
- [ ] `L2` Recursive resolver vs authoritative name server.
- [ ] `L2` A vs CNAME: why can't you put a CNAME on the zone apex, and what do providers do instead? ↳ CNAME can't coexist with SOA/NS; ALIAS/ANAME/flattening
- [ ] `L2` What are TXT records used for in practice? ↳ domain verification, SPF, DKIM, DMARC, ACME DNS-01
- [ ] `L2` Where is DNS cached along the way? ↳ browser, OS, resolver, app runtime (JVM!), connection pools
- [ ] `L2` You changed a DNS record and half the users still hit the old server an hour later. Why? ↳ TTL caches, resolvers ignoring TTL, long-lived connections
- [ ] `L2` How do you lower risk before migrating a domain to new servers? ↳ drop TTL days before, switch, raise TTL after
- [ ] `L2` What is DNS-based load balancing (round-robin, weighted, latency-based, geo)? What are its weaknesses? ↳ client caching, no health awareness, uneven
- [ ] `L2` How do containers in Docker Compose find each other by name? (Tie to Docker DNS.)
- [ ] `L2` What is negative caching (NXDOMAIN cached)? How can it bite you right after you create a record?
- [ ] `L2` What do `dig +short`, `dig +trace` and `dig @8.8.8.8` show?
- [ ] `L2` What is reverse DNS (PTR) and who uses it? ↳ mail servers, logs
- [ ] `L3` What is DNSSEC and what does it not protect?
- [ ] `L3` DNS over HTTPS / over TLS: why did they appear, and how do they change enterprise visibility?
- [ ] `L3` What is DNS cache poisoning (Kaminsky attack) and what mitigates it? ↳ random source port + txn ID, DNSSEC
- [ ] `L3` Your service gets intermittent 5-second delays on outbound calls in Kubernetes/Docker. Suspect DNS — why? ↳ `ndots`, search domains, conntrack race, A+AAAA parallel lookups
- [ ] `L3` What happens to your service when the DNS provider goes down (Dyn 2016)? How do you design for it?
- [ ] `L3` What is the HTTPS/SVCB record type and what does it add?
- [ ] `L3` Why should your app re-resolve DNS for long-lived connection pools, and what breaks if it never does?

## 14.7 TLS, certificates, SNI and mTLS
**Learn:** https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/ · hpbn.co ch.4 "Transport Layer Security" · https://tls13.xargs.org (every byte explained) · https://www.cloudflare.com/learning/access-management/what-is-mutual-tls/ · https://letsencrypt.org/how-it-works/
- [ ] `L1` What does TLS give you? ↳ confidentiality, integrity, server authentication
- [ ] `L1` HTTPS = HTTP + ? Which port?
- [ ] `L1` How does TLS prove the server's identity?
- [ ] `L1` What is a certificate? What is inside it? ↳ subject/SAN, public key, issuer, validity, signature
- [ ] `L1` What is a certificate authority (CA)?
- [ ] `L2` Walk through the TLS 1.2 handshake.
- [ ] `L2` Walk through the TLS 1.3 handshake. What got faster and what got removed? ↳ 1-RTT, key share in ClientHello, no RSA key exchange, AEAD only
- [ ] `L2` Asymmetric vs symmetric crypto in TLS: which is used for what, and why both?
- [ ] `L2` What is the chain of trust? Leaf, intermediate, root.
- [ ] `L2` Your service works in the browser but `curl` / Python `requests` says "unable to get local issuer certificate". Why? ↳ server not sending intermediate cert; incomplete chain
- [ ] `L2` What is SNI and why is it needed? ↳ many HTTPS sites on one IP; hostname in ClientHello
- [ ] `L2` What is forward secrecy and which key exchange gives it? ↳ ephemeral (EC)DHE
- [ ] `L2` What is mTLS? Where would you use it? ↳ service-to-service auth, zero trust, service mesh
- [ ] `L2` What is Let's Encrypt? How does the ACME protocol prove you own a domain? ↳ HTTP-01, DNS-01, TLS-ALPN-01 challenges
- [ ] `L2` HTTP-01 vs DNS-01 challenge: when do you need DNS-01? ↳ wildcard certs, no public port 80
- [ ] `L2` What is TLS termination? Where do you terminate TLS in your stack and is traffic re-encrypted behind it?
- [ ] `L2` What is ALPN?
- [ ] `L2` Your cert expired at 3 am and the site is down. How do you prevent this forever? ↳ auto-renewal (certbot/cert-manager), expiry monitoring alerts
- [ ] `L2` What is a wildcard certificate and what are its risks?
- [ ] `L2` How do you inspect a server's certificate from the command line? ↳ `openssl s_client -connect host:443 -servername host`
- [ ] `L3` What is TLS session resumption? Session IDs vs tickets vs PSK. What is 0-RTT and why can it be replayed?
- [ ] `L3` How is a certificate revoked? CRL vs OCSP vs OCSP stapling, and why revocation is "broken".
- [ ] `L3` What is Certificate Transparency and how does it catch mis-issued certificates?
- [ ] `L3` What is certificate pinning, and why did browsers drop HPKP?
- [ ] `L3` What is Encrypted Client Hello (ECH) and what does it hide that SNI leaks?
- [ ] `L3` How does a corporate TLS-inspecting proxy work, and why does it break pinned clients?
- [ ] `L3` What does TLS cost in CPU and latency today, and is "TLS is slow" still true?
- [ ] `L3` How would you rotate the private key and certificate of a high-traffic service with zero downtime?

## 14.8 HTTP versions — 1.0, 1.1, 2 and 3 (QUIC)
**Learn:** hpbn.co ch.11 "HTTP/1.X" + ch.12 "HTTP/2" · https://www.cloudflare.com/learning/performance/what-is-http3/ · https://http3-explained.haxx.se · Hussein Nasser "HTTP/1 vs HTTP/2 vs HTTP/3" (YouTube) · RFC 9113 (HTTP/2), RFC 9114 (HTTP/3)
- [ ] `L1` What changed from HTTP/1.0 to HTTP/1.1? ↳ persistent connections, Host header, chunked encoding, pipelining
- [ ] `L1` Why is the `Host` header mandatory in HTTP/1.1?
- [ ] `L1` How does HTTP/2 improve on HTTP/1.1?
- [ ] `L1` What is HTTP/3 and what runs underneath it?
- [ ] `L2` What is HTTP keep-alive (persistent connection)? What did it fix?
- [ ] `L2` What is HTTP pipelining and why did browsers never really use it? ↳ responses must be in order; HOL blocking; broken proxies
- [ ] `L2` Why did browsers open 6 connections per host on HTTP/1.1? What hacks did that cause? ↳ domain sharding, sprites, concatenation
- [ ] `L2` HTTP/2 streams, frames and multiplexing: how do many requests share one connection?
- [ ] `L2` What is HPACK and why do headers need compressing? ↳ repeated cookies/user-agent; static + dynamic table, Huffman
- [ ] `L2` HTTP/2 fixed HTTP-level head-of-line blocking. Which head-of-line blocking is still left? ↳ TCP-level: one lost packet stalls all streams
- [ ] `L2` How does QUIC remove TCP head-of-line blocking? ↳ independent streams over UDP; loss only stalls its stream
- [ ] `L2` What is connection migration in QUIC and why does it matter on mobile? ↳ connection ID, survives Wi-Fi → 4G switch
- [ ] `L2` What is chunked transfer encoding? When does a server use it?
- [ ] `L2` What are range requests and `206 Partial Content`? Name a use. ↳ resume downloads, video seeking
- [ ] `L2` What is compression with `Accept-Encoding`/`Content-Encoding` (gzip, br, zstd)? When is it not worth it?
- [ ] `L2` What is HTTP/2 server push and why was it removed from browsers? What replaced it? ↳ wasted bytes, cache misses; 103 Early Hints
- [ ] `L2` What is `h2c` and when do you see it? ↳ HTTP/2 cleartext, behind proxies, gRPC internally
- [ ] `L3` What is HTTP/2 flow control and how is it different from TCP's?
- [ ] `L3` What are HTTP/2 stream priorities and why did they get simplified in RFC 9218?
- [ ] `L3` What is QPACK and why couldn't HTTP/3 reuse HPACK? ↳ HPACK assumes in-order delivery; QUIC streams arrive out of order
- [ ] `L3` What is the "HTTP/2 rapid reset" attack (2023) and how did servers fix it?
- [ ] `L3` Why might HTTP/3 be slower than HTTP/2 on some networks? ↳ UDP throttling, userspace CPU cost, fallback races
- [ ] `L3` Should your internal service-to-service traffic use HTTP/1.1, HTTP/2 or HTTP/3? Defend it.
- [ ] `L3` What is request smuggling and how do HTTP/1.1 proxies and `Content-Length`/`Transfer-Encoding` disagreements cause it?

## 14.9 HTTP semantics — methods, status codes, headers, REST
**Learn:** https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods · https://developer.mozilla.org/en-US/docs/Web/HTTP/Status · RFC 9110 "HTTP Semantics" (rfc-editor.org/rfc/rfc9110) · https://developer.mozilla.org/en-US/docs/Glossary/Idempotent
- [ ] `L1` List the HTTP methods and what each means.
- [ ] `L1` What is a safe method? What is an idempotent method? Which methods are each?
- [ ] `L1` PUT vs PATCH — which is idempotent?
- [ ] `L1` POST vs PUT.
- [ ] `L1` What are the five classes of status codes?
- [ ] `L1` 401 vs 403.
- [ ] `L1` 502 vs 503 vs 504.
- [ ] `L1` 200 vs 201 vs 202 vs 204: when do you return each?
- [ ] `L1` 301 vs 302 vs 307 vs 308. ↳ permanent/temporary; 307/308 keep method and body
- [ ] `L2` 400 vs 422: which do you return for a validation error, and what does FastAPI return by default?
- [ ] `L2` When do you return 409 Conflict? 410 Gone? 412 Precondition Failed? 415? 429?
- [ ] `L2` What headers should a 429 or 503 response carry? ↳ `Retry-After`, rate-limit headers
- [ ] `L2` Is DELETE idempotent if the second call returns 404? Explain.
- [ ] `L2` How do you make a POST (e.g. "create payment") safe to retry? ↳ Idempotency-Key header + stored result
- [ ] `L2` Why should a GET never change state? What breaks if it does? ↳ crawlers, prefetchers, caches, retries
- [ ] `L2` What are `Content-Type` and `Accept`? What is content negotiation?
- [ ] `L2` What is `Content-Length`, and what happens when it lies?
- [ ] `L2` What are the `Authorization` header schemes you have used? ↳ Bearer, Basic, API key headers
- [ ] `L2` Which headers carry the client's real IP through proxies, and why can't you trust them blindly? ↳ X-Forwarded-For, Forwarded; trust only your proxy's hop
- [ ] `L2` What is the `OPTIONS` method used for?
- [ ] `L2` What is `HEAD` used for?
- [ ] `L2` What makes an API "RESTful"? Resources, representations, statelessness, uniform interface.
- [ ] `L2` What does "stateless" mean in REST, and does using JWT/cookies break it?
- [ ] `L2` What is HATEOAS, and does anyone actually do it?
- [ ] `L3` What happens to a POST if the client times out after the server committed? Design for it.
- [ ] `L3` How do retries at the load balancer interact with non-idempotent methods? ↳ LBs/proxies should not retry POST after bytes sent
- [ ] `L3` What is `Expect: 100-continue` and when does it help?
- [ ] `L3` Why do some APIs return 200 with an error body, and why is that bad for monitoring and caches?
- [ ] `L3` What are trailers in HTTP, and which protocol depends on them? ↳ gRPC status in HTTP/2 trailers

## 14.10 Caching headers, ETags, cookies and CORS
**Learn:** https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching · https://web.dev/articles/http-cache · https://developer.mozilla.org/en-US/docs/Web/HTTP/Conditional_requests · https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS · https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies · https://web.dev/articles/samesite-cookies-explained
- [ ] `L1` What does `Cache-Control: max-age=3600` do?
- [ ] `L1` `no-cache` vs `no-store`. ↳ no-cache = revalidate every time; no-store = never store
- [ ] `L1` What is an ETag?
- [ ] `L1` What is a `304 Not Modified` and how does the client get one?
- [ ] `L1` What is the same-origin policy? What counts as the same origin? ↳ scheme + host + port
- [ ] `L1` What is CORS?
- [ ] `L1` What do `HttpOnly`, `Secure` and `SameSite` do on a cookie?
- [ ] `L2` `If-None-Match` vs `If-Modified-Since`. Strong vs weak ETags.
- [ ] `L2` `private` vs `public`, and `s-maxage`: browser cache vs shared cache (CDN).
- [ ] `L2` What does the `Vary` header do, and how can it destroy your CDN hit rate? ↳ cache key includes those headers; Vary: User-Agent / Cookie
- [ ] `L2` What is `stale-while-revalidate` and `stale-if-error`?
- [ ] `L2` How do you cache static assets "forever" but still ship new versions? ↳ content hash in filename + immutable, short TTL HTML
- [ ] `L2` How do you use ETags for optimistic concurrency on updates? ↳ If-Match → 412 if changed
- [ ] `L2` Explain CORS preflight: when does the browser send `OPTIONS`, and what must the server answer?
- [ ] `L2` What is a "simple request" in CORS?
- [ ] `L2` Why can't you use `Access-Control-Allow-Origin: *` with credentials?
- [ ] `L2` Is CORS a server-side security feature? Can `curl` ignore it? ↳ browser-enforced; protects users, not your API
- [ ] `L2` Your frontend gets a CORS error but the server log shows 200. What happened?
- [ ] `L2` `SameSite=Strict` vs `Lax` vs `None`. Which does the browser default to?
- [ ] `L2` What is CSRF and how do SameSite cookies and CSRF tokens stop it?
- [ ] `L2` Cookie `Domain` and `Path` attributes: how do they scope a cookie? First-party vs third-party cookies.
- [ ] `L2` Cookies vs `Authorization` header vs localStorage for tokens: trade-offs.
- [ ] `L3` What does `Access-Control-Max-Age` do and why does it matter for latency?
- [ ] `L3` An authenticated API response got cached by the CDN and shown to another user. How did it happen and how do you prevent it?
- [ ] `L3` Why do heuristic caches cache responses with no `Cache-Control` at all? ↳ Last-Modified heuristic (10%)
- [ ] `L3` What is a cookie prefix (`__Host-`, `__Secure-`)?
- [ ] `L3` How does CHIPS / partitioned cookies change third-party cookies?

## 14.11 WebSockets — protocol, building one, scaling
**Learn:** hpbn.co ch.17 "WebSocket" · RFC 6455 (rfc-editor.org/rfc/rfc6455) · https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_servers · https://nginx.org/en/docs/http/websocket.html · https://ably.com/topic/websockets
- [ ] `L1` What is a WebSocket? How is it different from HTTP request/response?
- [ ] `L1` How does a WebSocket connection start? ↳ HTTP/1.1 GET with `Upgrade: websocket`, `101 Switching Protocols`
- [ ] `L1` `ws://` vs `wss://`.
- [ ] `L1` Is a WebSocket full-duplex?
- [ ] `L1` Text vs binary frames: which did you use for audio?
- [ ] `L2` Walk through the opening handshake headers. ↳ Upgrade, Connection, Sec-WebSocket-Key, Version 13, Sec-WebSocket-Accept
- [ ] `L2` How is `Sec-WebSocket-Accept` computed, and what does it prove? ↳ base64(SHA-1(key + fixed GUID)); server speaks WebSocket, not cache
- [ ] `L2` What does a WebSocket frame look like? ↳ FIN, opcode, mask bit, payload length (7/16/64-bit), masking key
- [ ] `L2` List the opcodes. ↳ continuation 0, text 1, binary 2, close 8, ping 9, pong A
- [ ] `L2` Why must the client mask frames, and why doesn't the server? ↳ cache-poisoning attack on intermediaries
- [ ] `L2` What are ping and pong frames for? Who sends them, and what if a pong never comes?
- [ ] `L2` Walk through the closing handshake. What do close codes 1000, 1001, 1006, 1008, 1011 mean? ↳ 1006 = abnormal, never sent on wire
- [ ] `L2` What is fragmentation (continuation frames) and when is it used?
- [ ] `L2` What are subprotocols (`Sec-WebSocket-Protocol`)? Give an example.
- [ ] `L2` How do you authenticate a WebSocket when browsers can't set custom headers on it? ↳ cookie, short-lived token in query/first message, subprotocol hack
- [ ] `L2` What nginx config do you need to proxy WebSockets? ↳ `proxy_http_version 1.1`, Upgrade/Connection headers, long `proxy_read_timeout`
- [ ] `L2` How do you detect a dead client connection on the server side? ↳ app-level ping with timeout; TCP alone may not notice
- [ ] `L2` How do clients reconnect safely? ↳ exponential backoff + jitter, resume token / last-seen id
- [ ] `L2` What is backpressure on a WebSocket? What happens when the client reads slower than you send? ↳ send buffer grows, `bufferedAmount`; drop, pause or disconnect
- [ ] `L2` How do you send a message to a user connected to a different server? ↳ pub/sub (Redis), connection registry, routing
- [ ] `L2` Why do WebSockets need sticky sessions (or not) behind a load balancer?
- [ ] `L2` What happens to open WebSockets when you deploy a new version? How do you drain? ↳ stop accepting, send close 1001/1012, client reconnects elsewhere
- [ ] `L2` socket.io vs raw WebSocket: what does socket.io add, and why might you avoid it? ↳ rooms, acks, reconnect, fallback; custom protocol, not plain WS
- [ ] `L3` Build a WebSocket server from scratch on a raw TCP socket, without libraries. What steps do you implement? ↳ parse HTTP upgrade, compute accept, frame parse/unmask, ping, close
- [ ] `L3` How do you parse a frame whose payload length is 126 or 127?
- [ ] `L3` What is `permessage-deflate`, and why might you disable it for audio or at scale? ↳ binary audio barely compresses; per-connection memory
- [ ] `L3` How do you scale to 1M concurrent WebSocket connections? ↳ epoll, FDs/ulimit, memory per conn, many nodes, LB, pub/sub fan-out
- [ ] `L3` How much memory does one idle WebSocket cost in Python/Node, and what dominates it?
- [ ] `L3` WebSocket over HTTP/2 (RFC 8441): what changes? ↳ extended CONNECT; many WS on one connection
- [ ] `L3` What is WebTransport and when might it replace WebSockets?
- [ ] `L3` At AiRA, one WebSocket carries audio up and audio/text down. Why one socket instead of separate STT/TTS connections?
- [ ] `L3` How do you design ordering, acks and resume for messages over WebSocket when TCP already guarantees order? ↳ order only per connection; reconnect loses in-flight; app seq numbers
- [ ] `L3` How do you load-test WebSocket servers? What do you measure?

## 14.12 SSE, long polling, gRPC and WebRTC
**Learn:** https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events · https://ably.com/blog/websockets-vs-sse · hpbn.co ch.15–16 (XHR polling, SSE) + ch.18 (WebRTC) · https://grpc.io/docs/what-is-grpc/core-concepts/ · https://webrtc.org/getting-started/peer-connections · https://bloggeek.me (WebRTC)
- [ ] `L1` Short polling vs long polling vs SSE vs WebSockets vs WebRTC: one line each.
- [ ] `L1` What is Server-Sent Events (SSE)? What content type does it use? ↳ `text/event-stream`
- [ ] `L1` What is gRPC? What does it run on?
- [ ] `L1` What is WebRTC?
- [ ] `L2` SSE vs WebSocket for streaming LLM tokens: which and why?
- [ ] `L2` How does SSE reconnect and resume? ↳ `id:` field, `Last-Event-ID` header, `retry:`
- [ ] `L2` Your SSE stream arrives all at once at the end when behind nginx. Why? ↳ proxy buffering/gzip; `X-Accel-Buffering: no`, `proxy_buffering off`
- [ ] `L2` What is the 6-connections-per-domain limit problem with SSE on HTTP/1.1?
- [ ] `L2` How does long polling work, and what does it cost the server?
- [ ] `L2` Why does gRPC need HTTP/2? ↳ multiplexed streams, binary framing, trailers for status
- [ ] `L2` What are unary, server-streaming, client-streaming and bidirectional gRPC calls?
- [ ] `L2` gRPC vs REST/JSON between services: trade-offs.
- [ ] `L2` Why is gRPC awkward to load-balance with an L4 load balancer? ↳ one long HTTP/2 conn pins to one backend; need L7/client-side LB
- [ ] `L2` What is gRPC-Web and why does the browser need it?
- [ ] `L2` What are gRPC deadlines and how do they propagate?
- [ ] `L2` WebRTC: what are ICE, STUN and TURN?
- [ ] `L2` What is signaling in WebRTC, and why is it not part of the standard? ↳ exchange SDP + ICE candidates over your own channel (often WebSocket)
- [ ] `L2` What is SDP?
- [ ] `L2` When does WebRTC need a TURN server, and what does TURN cost you? ↳ symmetric NAT/firewalls; relays all media, bandwidth bill
- [ ] `L3` What do SRTP and DTLS do in WebRTC?
- [ ] `L3` Mesh vs SFU vs MCU for group calls.
- [ ] `L3` Would you rebuild AiRA's voice on WebRTC? What would you gain (latency, loss handling, echo cancellation) and what would it cost?
- [ ] `L3` How do voice AI products (e.g. OpenAI Realtime, LiveKit) use WebRTC vs WebSocket for audio?
- [ ] `L3` What are ICE candidate types (host, srflx, relay) and how is the best pair chosen?
- [ ] `L3` How would you stream LLM output to a mobile app on a flaky network with no lost or duplicated tokens?

## 14.13 Load balancers, reverse proxies, CDNs and anycast
**Learn:** https://www.cloudflare.com/learning/performance/what-is-load-balancing/ · https://nginx.org/en/docs/http/ngx_http_proxy_module.html · https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/ · https://www.cloudflare.com/learning/cdn/what-is-a-cdn/ · https://www.cloudflare.com/learning/cdn/glossary/anycast-network/
- [ ] `L1` What is a load balancer?
- [ ] `L1` L4 vs L7 load balancing. ↳ L4 sees IP/port, forwards TCP/UDP; L7 sees HTTP, routes by path/header
- [ ] `L1` What is a reverse proxy? Forward proxy? Difference?
- [ ] `L1` What is a CDN?
- [ ] `L1` Name the common load-balancing algorithms. ↳ round-robin, least connections, weighted, IP hash, consistent hash, P2C
- [ ] `L2` What can an L7 load balancer do that an L4 cannot? What does it cost?
- [ ] `L2` AWS ALB vs NLB; Azure Application Gateway vs Azure Load Balancer: which for WebSockets, gRPC, static IPs?
- [ ] `L2` Active vs passive health checks. What should a health check endpoint check?
- [ ] `L2` What are sticky sessions? Cookie vs IP-hash stickiness. Why do they hurt?
- [ ] `L2` What does nginx do in front of a FastAPI/uvicorn app? ↳ TLS termination, buffering slow clients, static files, limits, routing
- [ ] `L2` Write the key nginx directives for a reverse proxy: `proxy_pass`, `upstream`, headers, timeouts, `client_max_body_size`.
- [ ] `L2` What is `413 Request Entity Too Large` from nginx and how do you fix it?
- [ ] `L2` What are `proxy_connect_timeout`, `proxy_read_timeout` and `proxy_send_timeout`? Which one kills idle WebSockets?
- [ ] `L2` How do you keep connections from nginx to upstream alive? ↳ `upstream { keepalive N; }`, HTTP/1.1, clear Connection header
- [ ] `L2` What is a slowloris attack and how do proxies protect the app from slow clients?
- [ ] `L2` What is connection draining / deregistration delay?
- [ ] `L2` How does a CDN decide what to cache? What is the cache key?
- [ ] `L2` What is anycast? How does it route users to the nearest PoP? ↳ same IP announced from many places via BGP
- [ ] `L2` What is an API gateway, and how is it different from a load balancer?
- [ ] `L2` What is the PROXY protocol, and when do you need it? ↳ pass client IP through an L4 LB
- [ ] `L3` How does one load balancer avoid being a single point of failure? ↳ multiple nodes + VIP/keepalived/anycast, DNS, managed LB
- [ ] `L3` What is direct server return (DSR)?
- [ ] `L3` How do you load-balance long-lived connections (WebSockets, gRPC) so new servers actually get traffic?
- [ ] `L3` What is the "thundering herd" after a CDN cache expires, and what is request coalescing?
- [ ] `L3` What is a service mesh / sidecar proxy (Envoy) and what network jobs does it take from your code?
- [ ] `L3` How would you do a canary release at the load balancer?
- [ ] `L3` Explain timeouts at each hop: client → CDN → LB → nginx → app → DB. How should they relate? ↳ outer > inner; avoid orphaned work
- [ ] `L3` What does consistent hashing at the LB give you, and when is it worth it?

## 14.14 Latency, timeouts, retries and network failures
**Learn:** DDIA ch8 "Unreliable Networks" (pdf p291–300) · https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/ · https://gist.github.com/jboner/2841832 (latency numbers) · *Release It!* ch.5 "Stability Patterns"
- [ ] `L1` Latency vs bandwidth vs throughput.
- [ ] `L1` What is RTT?
- [ ] `L1` What is a network partition?
- [ ] `L1` Why do you always set a timeout on network calls?
- [ ] `L2` Give the rough latency numbers: memory read, SSD read, same-datacenter round trip, cross-continent round trip. ↳ ~100 ns, ~100 µs, ~0.5 ms, ~150 ms
- [ ] `L2` What is the speed-of-light limit for Mumbai ↔ US-East and what RTT do you see in practice?
- [ ] `L2` Connect timeout vs read timeout vs total timeout. How do you pick values?
- [ ] `L2` What is exponential backoff with jitter, and why jitter? ↳ avoid synchronized retry storms
- [ ] `L2` What is a retry storm / retry amplification across layers? ↳ 3 layers × 3 retries = 27× load
- [ ] `L2` Which errors are safe to retry and which are not?
- [ ] `L2` What is a circuit breaker? States?
- [ ] `L2` A call timed out. Did the server do the work? What does that mean for your design? ↳ unknown outcome; idempotency
- [ ] `L2` Why does a connection pool help? What are its knobs? ↳ skip handshakes/slow start; max size, idle timeout, max lifetime
- [ ] `L2` How many uvicorn workers would you run on a 4-core box, and how does that relate to connection pool sizes?
- [ ] `L2` What is tail latency (p99) and why does fan-out make it worse?
- [ ] `L2` What is a retry budget?
- [ ] `L3` What is hedging (backup requests), and when is it worth the extra load?
- [ ] `L3` What is a gray failure / partial partition, and why are they harder than clean outages?
- [ ] `L3` Why can't a node tell a slow peer from a dead one? What does that imply for failure detectors? ↳ unbounded delays; timeouts are guesses; phi accrual
- [ ] `L3` Deadline propagation: how do you stop downstream work after the caller has given up?
- [ ] `L3` Packet loss of 1% — what does it do to TCP throughput and to a voice call?
- [ ] `L3` What is Little's law and how does it size a connection pool?
- [ ] `L3` What are conntrack table limits and how does "nf_conntrack: table full" show up?
- [ ] `L3` Your voice pipeline calls STT, LLM and TTS providers. How do you budget timeouts so the user hears something within 1 s?

## 14.15 Debugging tools and scenarios
**Learn:** Julia Evans "Bite Size Networking" + "tcpdump" zines (wizardzines.com) · `Linux Commands/6. linux commands.txt` (lsof) · https://everything.curl.dev · https://www.wireshark.org/docs/wsug_html_chunked/ · `man ss`, `man mtr`
- [ ] `L1` What does `ping` tell you, and what doesn't it?
- [ ] `L1` What does `traceroute` show? How does it work? ↳ increasing TTL, ICMP time-exceeded per hop
- [ ] `L1` What does `curl -v` show you?
- [ ] `L1` What does `dig` do? `nslookup`?
- [ ] `L1` How do you see which process is listening on port 8080? ↳ `ss -ltnp`, `lsof -i :8080`
- [ ] `L2` Read this `curl -v` output: where do you see DNS, connect, TLS, request headers and response headers?
- [ ] `L2` How do you time each phase of a request with curl? ↳ `-w` with time_namelookup, time_connect, time_appconnect, time_starttransfer
- [ ] `L2` How do you send a request to a specific IP while keeping the right Host/SNI? ↳ `curl --resolve host:443:IP`
- [ ] `L2` `ss` vs `netstat`. What do the `-t -u -l -n -p -a` flags do?
- [ ] `L2` What do Recv-Q and Send-Q mean in `ss` for a listening socket vs an established one?
- [ ] `L2` How do you count connections by state on a server? ↳ `ss -tan | awk '{print $1}' | sort | uniq -c`
- [ ] `L2` What is `mtr` and why is it better than traceroute for intermittent loss?
- [ ] `L2` How do you capture traffic on port 443 with `tcpdump` and save it for Wireshark? ↳ `tcpdump -i any port 443 -w out.pcap`
- [ ] `L2` What can and can't you see in a pcap of HTTPS traffic? How do you decrypt your own? ↳ SNI, sizes, timing; SSLKEYLOGFILE
- [ ] `L2` How do you test if a TCP port is open from a container with no curl? ↳ `nc -zv`, bash `/dev/tcp`, `telnet`
- [ ] `L2` What do `openssl s_client -connect` and `-showcerts` tell you?
- [ ] `L2` How do you check certificate expiry from the command line?
- [ ] `L2` What do `ip addr`, `ip route` and `ip neigh` show?
- [ ] `L2` Port 8080 is already in use. Find and stop the process.
- [ ] `L3` Users say the API is "slow sometimes". Walk through your network investigation from client to server.
- [ ] `L3` Requests from one AZ to the DB intermittently take 3 s. 3 s exactly. What does that number suggest? ↳ SYN retransmit timeout (1 s, 3 s); packet loss / backlog
- [ ] `L3` Large file uploads hang but small ones work, only over the VPN. What do you suspect? ↳ MTU/PMTUD black hole
- [ ] `L3` Your service gets "connection reset by peer" under load but not at low traffic. List the causes you check. ↳ backlog overflow, LB idle timeout, keep-alive mismatch, conntrack
- [ ] `L3` Upstream returns 502 from nginx only every few minutes. Suspect keep-alive timeouts — explain the race. ↳ upstream closes idle conn as nginx reuses it; upstream timeout > proxy's
- [ ] `L3` How would you find which hop adds 200 ms of latency between your VM and a third-party API?
- [ ] `L3` What is `tcptraceroute` / `traceroute -T` and why use TCP instead of ICMP?
- [ ] `L3` How do you inspect network traffic inside a running container's network namespace? ↳ `nsenter -t <pid> -n tcpdump`, sidecar `--net container:`
- [ ] `L3` How do you reproduce bad network conditions (latency, loss) locally? ↳ `tc qdisc netem`, toxiproxy

## 14.16 Rapid-fire round
- [ ] `L1` Default port for HTTP? HTTPS? SSH? DNS? Postgres? Redis?
- [ ] `L1` How many bits in an IPv4 address? IPv6?
- [ ] `L1` How many addresses in a `/24`?
- [ ] `L1` TCP or UDP: DNS queries?
- [ ] `L1` Which side of a TCP connection ends up in TIME_WAIT?
- [ ] `L1` What does CLOSE_WAIT usually mean?
- [ ] `L1` What does RST mean?
- [ ] `L1` What is the default MTU on Ethernet? ↳ 1500
- [ ] `L1` What does `TCP_NODELAY` disable?
- [ ] `L1` What status code does a WebSocket upgrade return?
- [ ] `L1` What is WebSocket opcode 9?
- [ ] `L1` What close code means "normal closure"?
- [ ] `L1` Is PUT idempotent? Is POST?
- [ ] `L1` Which status code means "too many requests"?
- [ ] `L1` 401 or 403 for a logged-in user without permission?
- [ ] `L1` What does a 304 mean?
- [ ] `L1` What does SNI stand for?
- [ ] `L1` How many round trips is a full TLS 1.3 handshake?
- [ ] `L1` What transport does HTTP/3 use?
- [ ] `L1` What does a CNAME record point to?
- [ ] `L1` What does TTL mean in DNS?
- [ ] `L1` Which record type does Let's Encrypt DNS-01 use? ↳ TXT
- [ ] `L1` What does STUN discover?
- [ ] `L1` What does TURN do?
- [ ] `L1` L4 or L7: path-based routing?
- [ ] `L1` What is anycast in one line?
- [ ] `L1` Which header tells a CDN response varies by encoding?
- [ ] `L1` What does `Access-Control-Allow-Origin` control?
- [ ] `L1` Which cookie flag stops JavaScript from reading it?
- [ ] `L1` Which tool shows open sockets on Linux today: `ss` or `netstat`?
- [ ] `L1` What is a 502 Bad Gateway, in one line?
- [ ] `L1` What is RTT across the same data center, roughly?
- [ ] `L1` What is jitter?
