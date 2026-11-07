# 9. PostgreSQL and SQL

Every backend round has a database part: write a query live, explain why a query is slow, and say what happens
inside Postgres when two transactions touch the same row. A 3-year engineer must read an `EXPLAIN` plan, pick the
right index, explain MVCC and isolation levels, and change a big table without downtime. Syllabus: 2A PostgreSQL
(`../../syllabus.html`).

## 9.1 SQL fundamentals — joins, NULLs, grouping, subqueries
**Learn:** DDIA ch2 "Query Languages for Data" (pdf p64–67) · https://www.postgresql.org/docs/current/tutorial-select.html · https://www.postgresql.org/docs/current/queries-table-expressions.html · https://leetcode.com/studyplan/top-sql-50/
- [ ] `L1` In what logical order is a `SELECT` evaluated? ↳ FROM/JOIN, WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY, LIMIT
- [ ] `L1` INNER vs LEFT vs RIGHT vs FULL OUTER vs CROSS JOIN: which rows does each return?
- [ ] `L1` WHERE vs HAVING.
- [ ] `L1` `COUNT(*)` vs `COUNT(col)` vs `COUNT(DISTINCT col)`.
- [ ] `L1` Why does `WHERE col = NULL` return no rows? ↳ three-valued logic; NULL = NULL is unknown; use IS NULL
- [ ] `L1` UNION vs UNION ALL: which is faster and why?
- [ ] `L1` DELETE vs TRUNCATE vs DROP.
- [ ] `L1` What do `COALESCE` and `NULLIF` do?
- [ ] `L2` Write "employees who earn more than their manager" with a self join.
- [ ] `L2` Write "customers who never placed an order" with LEFT JOIN, NOT EXISTS and NOT IN. What is the NULL trap? ↳ NOT IN returns nothing if the subquery yields a NULL
- [ ] `L2` What is a correlated subquery? How does it execute, and how do you rewrite it as a join?
- [ ] `L2` You put a filter on the right table of a LEFT JOIN in WHERE instead of ON. What happens? ↳ NULL rows filtered out: it becomes an inner join
- [ ] `L2` Find duplicate emails in a `users` table.
- [ ] `L2` Delete duplicate rows, keeping the one with the lowest id.
- [ ] `L2` Write "second highest salary"; return NULL when there is none.
- [ ] `L2` What does `IS DISTINCT FROM` do and when do you need it?
- [ ] `L2` Pivot: orders per status per month as columns. ↳ SUM(CASE …) or COUNT(*) FILTER (WHERE …)
- [ ] `L2` What does `DISTINCT ON` do in Postgres? Give a use.
- [ ] `L3` A JOIN returns more rows than the left table has. Why, and how do you find the fan-out?
- [ ] `L3` `SUM(amount)` over orders joined to order items double-counts. How do you fix it? ↳ aggregate each side before joining, or use a subquery/CTE
- [ ] `L3` `timestamp` or `timestamptz`? What breaks with the wrong choice?
- [ ] `L3` Why can `SELECT *` hurt beyond network bytes? ↳ blocks index-only scans, detoasts big columns, breaks on schema change

## 9.2 Window functions, CTEs and classic SQL problems
**Learn:** DDIA ch2 "Graph queries in SQL" (pdf p74–77) · https://www.postgresql.org/docs/current/tutorial-window.html · https://www.postgresql.org/docs/current/queries-with.html · https://mode.com/sql-tutorial/sql-window-functions/ · https://datalemur.com
- [ ] `L1` What is a window function, and how is it different from GROUP BY?
- [ ] `L1` ROW_NUMBER vs RANK vs DENSE_RANK: what happens on ties?
- [ ] `L1` What do LAG and LEAD do?
- [ ] `L1` What is a CTE (`WITH` clause)?
- [ ] `L2` Top 3 salaries per department (top-N per group). Write it two ways. ↳ DENSE_RANK in a subquery; LATERAL join with LIMIT
- [ ] `L2` Running total of revenue per day, and per user.
- [ ] `L2` Month-over-month revenue growth in percent.
- [ ] `L2` 7-day moving average. What is the difference between a ROWS frame and a RANGE frame?
- [ ] `L2` Users active 3 or more days in a row (gaps and islands). ↳ date minus ROW_NUMBER is constant within a streak
- [ ] `L2` Find missing numbers in a sequence of invoice numbers.
- [ ] `L2` `INSERT … ON CONFLICT DO UPDATE` vs `DO NOTHING`. What is `EXCLUDED`?
- [ ] `L2` Is `ON CONFLICT` race-free under concurrency? What does it require? ↳ a unique index or constraint matching the conflict target
- [ ] `L2` Upsert vs `MERGE` (PG15): when would you use `MERGE`?
- [ ] `L2` Recursive CTE: all reports under a manager, or a whole comment thread.
- [ ] `L2` How do you stop a recursive CTE from looping forever on cyclic data? ↳ track visited path in an array; CYCLE clause (PG14)
- [ ] `L2` OFFSET pagination vs keyset (seek) pagination: why is `OFFSET 100000` slow? ↳ reads and throws away every skipped row
- [ ] `L2` Write keyset pagination ordered by `created_at DESC` with ties. ↳ row comparison (created_at, id) < ($1, $2) plus matching index
- [ ] `L3` Before PG12 a CTE was an "optimisation fence". What changed, and what do `MATERIALIZED` / `NOT MATERIALIZED` do?
- [ ] `L3` Keyset pagination cannot jump to page 50. How do you design the API and UI around that?
- [ ] `L3` `percentile_cont` vs `percentile_disc`: compute the median order value.
- [ ] `L3` What is a `LATERAL` join? Give a real use.
- [ ] `L3` Sessionize a clickstream: a new session starts after 30 minutes of inactivity.
- [ ] `L3` Distinct users over a rolling 30-day window: why is it hard in SQL? ↳ no DISTINCT in window functions; self-join, date series, or HLL

## 9.3 Schema design, normalization and constraints
**Learn:** DDIA ch2 "The object-relational mismatch" (pdf p50–52) + "Many-to-one and many-to-many relationships" (pdf p53–57) · https://www.postgresql.org/docs/current/ddl-constraints.html · https://wiki.postgresql.org/wiki/Don%27t_Do_This · https://www.rfc-editor.org/rfc/rfc9562 (UUIDv7)
- [ ] `L1` What is normalization? Explain 1NF, 2NF and 3NF in one line each.
- [ ] `L1` Primary key vs unique constraint vs unique index.
- [ ] `L1` What is a foreign key? What do `ON DELETE CASCADE`, `RESTRICT` and `SET NULL` do?
- [ ] `L1` Surrogate key vs natural key.
- [ ] `L1` Which constraints does Postgres support? ↳ NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, EXCLUDE
- [ ] `L2` Normalise this table: `orders(order_id, customer_name, customer_email, product_names_csv, total)`.
- [ ] `L2` When do you denormalise on purpose? Give an example and say how you keep the copy in sync.
- [ ] `L2` bigint identity vs UUIDv4 vs UUIDv7 as primary key: effect on index size and insert locality. ↳ random UUIDs scatter B-tree inserts; v7 is time-ordered
- [ ] `L2` `SERIAL` vs `GENERATED ALWAYS AS IDENTITY`.
- [ ] `L2` Model a many-to-many relation (students and courses). What columns go on the join table?
- [ ] `L2` How would you model polymorphic associations (comments on posts, photos and videos)? Trade-offs.
- [ ] `L2` Soft delete with a `deleted_at` column: what breaks? ↳ every query needs the filter; unique constraints; use partial unique index
- [ ] `L2` Multi-tenancy: shared tables with `tenant_id`, schema per tenant, database per tenant, row-level security.
- [ ] `L2` Design the schema for an e-commerce order system (orders, items, payments, inventory).
- [ ] `L2` Design the schema for a chat app (users, conversations, members, messages, read receipts).
- [ ] `L2` Design the schema for a hiring platform (jobs, candidates, applications, stages, referrals). Tie it to Jigsaw.
- [ ] `L2` Does Postgres index foreign keys for you? Should you? ↳ no; index them for joins and parent DELETE checks
- [ ] `L2` Storing money: why not `float`? `numeric` vs integer cents.
- [ ] `L2` `varchar(n)` vs `text` in Postgres.
- [ ] `L3` Prevent overlapping room bookings in the database itself. ↳ EXCLUDE USING gist on room and tstzrange with &&
- [ ] `L3` Enforce "one active subscription per user" without application code. ↳ partial unique index WHERE status = 'active'
- [ ] `L3` Postgres `ENUM` vs lookup table vs CHECK constraint: what is the migration pain of each?
- [ ] `L3` What are deferrable constraints and when do you need them?
- [ ] `L3` EAV (entity–attribute–value) vs JSONB for user-defined attributes.

## 9.4 Indexes — B-tree, multicolumn, partial, expression, covering
**Learn:** DBI ch2 "Ubiquitous B-Trees" (pdf p69–85) · DBI ch4 "Sibling Links" (pdf p114–115) · DDIA ch3 "B-trees" (pdf p99–103) + "Storing values within the index" (pdf p105–106) · https://use-the-index-luke.com · https://www.postgresql.org/docs/current/indexes.html
- [ ] `L1` What is an index, and what does it cost you?
- [ ] `L1` What is the default index type in Postgres? Why a B-tree and not a binary search tree? ↳ high fan-out, few pages per lookup, sorted for ranges
- [ ] `L1` What is a composite (multicolumn) index?
- [ ] `L2` How do a B-tree point lookup and a range scan work? Why are leaf pages linked?
- [ ] `L2` Index on `(a, b)`: which of `a = 1`, `b = 1`, `a = 1 AND b = 2`, `a > 1 AND b = 2` use it well? ↳ leftmost prefix; equality columns first, range column last
- [ ] `L2` How do you choose column order in a multicolumn index? ↳ equality before range, match ORDER BY, then selectivity
- [ ] `L2` Can an index serve `ORDER BY created_at DESC LIMIT 20`? What about `ORDER BY a ASC, b DESC`?
- [ ] `L2` What is a partial index? Give two real uses. ↳ WHERE status = 'pending'; unique among non-deleted rows
- [ ] `L2` What is an expression index? Example: case-insensitive email lookup. ↳ index on lower(email); query must use the same expression
- [ ] `L2` What is a covering index (`INCLUDE`), and how does it enable index-only scans?
- [ ] `L2` Postgres heap plus secondary indexes vs MySQL InnoDB clustered index: what differs on a lookup?
- [ ] `L2` What does `CLUSTER` do in Postgres, and why doesn't the table stay clustered?
- [ ] `L2` How does each extra index slow down writes? Think of a table with 8 indexes.
- [ ] `L2` When can adding an index make the whole system slower? ↳ write-heavy table, lost HOT updates, bloat, memory pressure
- [ ] `L2` How do you find unused and duplicate indexes? ↳ pg_stat_user_indexes idx_scan = 0; overlapping leading columns
- [ ] `L3` What are HOT (heap-only tuple) updates, and how do indexes prevent them? ↳ no indexed column changed and free space on page; fillfactor
- [ ] `L3` What is B-tree deduplication (PG13), and when does it help?
- [ ] `L3` What happens on a B-tree page split? Why do random UUID keys cause more splits than sequential ids?
- [ ] `L3` Separate indexes on `a` and `b` vs one on `(a, b)`: when does Postgres combine two indexes? ↳ BitmapAnd / BitmapOr of bitmap index scans
- [ ] `L3` An index on a boolean column: useless or useful? When is it useful? ↳ as a partial index on the rare value
- [ ] `L3` B-tree vs LSM tree: which suits write-heavy logs, and why does Postgres stay with B-trees? ↳ LSM: sequential writes, compaction; B-tree: predictable reads, in-place pages

## 9.5 Other index types — Hash, GIN, GiST, SP-GiST, BRIN
**Learn:** DDIA ch3 "Hash indexes" (pdf p92–96) + "Other indexing structures" (pdf p104–107) · https://www.postgresql.org/docs/current/indexes-types.html · https://www.postgresql.org/docs/current/brin-intro.html · https://www.postgresql.org/docs/current/pgtrgm.html
- [ ] `L1` Name the Postgres index types and one use for each.
- [ ] `L1` What is a GIN index, and what data is it for? ↳ inverted index: arrays, JSONB, tsvector full-text
- [ ] `L1` What is a BRIN index? ↳ min/max summary per block range; huge, physically ordered tables
- [ ] `L2` Hash index vs B-tree: when is hash worth it, and what can't it do? ↳ equality only: no ranges, sorting, uniqueness or multicolumn
- [ ] `L2` Why did people avoid hash indexes before PG10? ↳ not WAL-logged, so not crash-safe or replicated
- [ ] `L2` GIN on JSONB: `jsonb_ops` vs `jsonb_path_ops`. ↳ path_ops is smaller and faster but supports only containment
- [ ] `L2` Why are GIN inserts slow, and what do `fastupdate` and the pending list do?
- [ ] `L2` What is GiST good for? ↳ ranges, geometry/PostGIS, exclusion constraints, nearest-neighbour, trigrams
- [ ] `L2` GIN vs GiST for full-text search. ↳ GIN faster lookups, slower updates; GiST smaller, lossy, needs rechecks
- [ ] `L2` A 2 TB append-only events table is queried by time range. B-tree or BRIN? Why?
- [ ] `L2` When does a BRIN index stop helping? ↳ column not correlated with physical row order; scattered updates
- [ ] `L2` What is `pg_trgm`, and how does it let an index serve `LIKE '%phone%'`? ↳ trigram GIN/GiST index
- [ ] `L2` Why can't a normal B-tree help `LIKE '%phone%'`, yet it can help `LIKE 'phone%'`? ↳ leading wildcard leaves no sorted prefix to seek
- [ ] `L3` What is SP-GiST, and what data suits it? ↳ space-partitioned trees: quadtrees, k-d trees, radix tries
- [ ] `L3` How does `ORDER BY location <-> point LIMIT 10` use a GiST index (KNN search)?
- [ ] `L3` What is the `bloom` index extension for?
- [ ] `L3` How do pgvector's HNSW and IVFFlat fit into Postgres's index access method model?

## 9.6 When an index is not used
**Learn:** https://use-the-index-luke.com/sql/where-clause · https://www.postgresql.org/docs/current/indexes-bitmap-scans.html · https://www.postgresql.org/docs/current/planner-stats.html · https://www.postgresql.org/docs/current/sql-createstatistics.html
- [ ] `L1` You created an index and `EXPLAIN` still shows a Seq Scan. Name five reasons. ↳ low selectivity, tiny table, function on column, type mismatch, stale stats
- [ ] `L1` Why is a sequential scan sometimes faster than an index scan? ↳ sequential vs random I/O when many rows match
- [ ] `L2` `WHERE lower(email) = $1` with an index on `email`. Is it used? How do you fix it?
- [ ] `L2` `WHERE created_at::date = '2026-01-01'`: why no index, and how do you rewrite it as a range?
- [ ] `L2` `WHERE phone = 9876543210` on a `text` column. What happens?
- [ ] `L2` `WHERE a = 1 OR b = 2`: how can Postgres use indexes here, and when does it give up? ↳ BitmapOr if both indexed; otherwise rewrite as UNION
- [ ] `L2` Why are `!=`, `NOT IN` and `NOT LIKE` rarely index-friendly?
- [ ] `L2` `WHERE deleted_at IS NULL`: can a B-tree help? ↳ yes, Postgres B-trees store NULLs; partial index is better
- [ ] `L2` A query is fast in psql but slow from the app with bound parameters. Why? ↳ generic plan after 5 executions; plan_cache_mode
- [ ] `L2` Index on `(tenant_id, created_at)` but the query filters only on `created_at`. What happens?
- [ ] `L2` How do `random_page_cost` and `seq_page_cost` change index choice? Why lower `random_page_cost` on SSDs?
- [ ] `L2` `WHERE status = 'x' ORDER BY id LIMIT 10` walks the primary key index and is slow. Why? ↳ planner assumes matches are spread evenly; they cluster at the end
- [ ] `L3` How do you test "would this index help?" without building it on prod? ↳ hypopg hypothetical indexes; a prod-sized copy
- [ ] `L3` How do you discourage a plan while debugging? ↳ SET enable_seqscan = off in your session; pg_hint_plan; never globally
- [ ] `L3` Why might a B-tree on a `text` column not serve `LIKE 'abc%'`? ↳ non-C collation; use text_pattern_ops
- [ ] `L3` Correlated columns (city and zip) make the planner underestimate rows. How do you fix it? ↳ CREATE STATISTICS with dependencies, ndistinct or mcv
- [ ] `L3` `data->>'type' = 'x'` vs `data @> '{"type":"x"}'` on JSONB: which index does each need?

## 9.7 Reading EXPLAIN and the planner
**Learn:** https://www.postgresql.org/docs/current/using-explain.html · https://www.postgresql.org/docs/current/planner-stats.html · https://explain.dalibo.com · https://www.pgmustard.com/docs/explain · CMU 15-445 lectures "Query Execution" and "Join Algorithms" (YouTube)
- [ ] `L1` `EXPLAIN` vs `EXPLAIN ANALYZE`. What is the danger of `EXPLAIN ANALYZE DELETE …`? ↳ ANALYZE really runs it; wrap in BEGIN … ROLLBACK
- [ ] `L1` What do the two numbers in `cost=0.43..8.45` mean? ↳ startup cost and total cost, in planner units
- [ ] `L1` What does `rows=` mean in the estimate part vs the actual part?
- [ ] `L1` Seq Scan, Index Scan, Index Only Scan, Bitmap Heap Scan: one line each.
- [ ] `L2` What does the `BUFFERS` option add? Explain `shared hit`, `read`, `dirtied` and `written`.
- [ ] `L2` When does Postgres pick a bitmap scan over a plain index scan? ↳ medium selectivity; sorts row locations to read heap pages in order
- [ ] `L2` What is "Rows Removed by Filter" telling you?
- [ ] `L2` What is a lossy bitmap heap scan, and why is there a `Recheck Cond`? ↳ bitmap exceeds work_mem, keeps pages not rows
- [ ] `L2` An Index Only Scan shows `Heap Fetches: 50000`. Why, and how do you fix it? ↳ visibility map not set; run VACUUM
- [ ] `L2` Nested loop vs hash join vs merge join: when does the planner pick each?
- [ ] `L2` Estimated rows=1, actual rows=200000. What does that cause, and what do you do? ↳ bad join choice; ANALYZE, raise statistics target, extended stats
- [ ] `L2` What does `loops=` mean, and how do you get the total time of a node?
- [ ] `L2` What do `Sort Method: external merge Disk` and `HashAggregate … Batches: 8` mean? ↳ spilled to disk; raise work_mem for that query
- [ ] `L2` What does the `ANALYZE` command do, and when does autovacuum run it?
- [ ] `L2` What is `default_statistics_target`, and when do you raise it for one column?
- [ ] `L2` What are `most_common_vals` and `histogram_bounds` in `pg_stats` used for?
- [ ] `L2` Read a plan aloud: which node is the slowest, and is it the one with the highest cost?
- [ ] `L3` How does the planner estimate `WHERE a = 1 AND b = 2`, and why is it often wrong? ↳ assumes independence and multiplies selectivities
- [ ] `L3` What is a Gather node? Which settings control parallel query?
- [ ] `L3` What is JIT compilation in Postgres, and when does it make short queries slower?
- [ ] `L3` What are `join_collapse_limit` and GEQO, and when do they matter?
- [ ] `L3` Why can `EXPLAIN ANALYZE` time differ from the real query time? ↳ per-row timing overhead; excludes network and client time
- [ ] `L3` What does a Memoize node (PG14) cache?
- [ ] `L3` How do you capture plans of slow queries in production automatically? ↳ auto_explain with log_min_duration

## 9.8 Query optimization, N+1 and ORM pitfalls
**Learn:** https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html · https://www.prisma.io/docs/orm/prisma-client/queries/query-optimization-performance · https://github.com/graphql/dataloader · https://use-the-index-luke.com/sql/join · DDIA ch3 "Aggregation: Data cubes and materialized views" (pdf p120–121)
- [ ] `L1` What is the N+1 query problem?
- [ ] `L1` How does eager loading fix N+1?
- [ ] `L2` SQLAlchemy `joinedload` vs `selectinload`: when each? ↳ joinedload for many-to-one; selectinload for collections avoids row explosion
- [ ] `L2` Prisma / TypeORM: how do `include` and relations become SQL, and where does N+1 hide?
- [ ] `L2` How do you find N+1 queries in a running app? ↳ queries per request, APM traces, SQL logging, pg_stat_statements calls
- [ ] `L2` What is DataLoader, and how does it batch?
- [ ] `L2` When would you drop down from the ORM to raw SQL?
- [ ] `L2` Raw SQL: how do you avoid SQL injection? Why can't you bind a table name or ORDER BY column? ↳ bind params for values; allow-list identifiers
- [ ] `L2` One INSERT per row vs multi-row VALUES vs `COPY`: rough speed difference?
- [ ] `L2` Update 1M rows in one statement or in batches? ↳ one statement: long locks, WAL burst, replica lag; batch by key range
- [ ] `L2` `SELECT count(*)` on a big table is slow. Why, and what are the alternatives? ↳ MVCC visibility checks; reltuples estimate, counter table
- [ ] `L2` The ORM opens a transaction per request and holds it during an HTTP call to another service. What breaks?
- [ ] `L2` Aggregation in application code vs in SQL: when is each right?
- [ ] `L2` What is a materialized view? How do you refresh it, and what does `REFRESH … CONCURRENTLY` need? ↳ a unique index on the view
- [ ] `L2` Triggers and stored functions: when do they help, and why do teams keep business logic out of them?
- [ ] `L2` What do prepared statements save?
- [ ] `L3` Rewrite a correlated subquery that runs once per row into one join plus GROUP BY.
- [ ] `L3` How do you stop lazy loading inside serializers from reaching production? ↳ lazy='raise', query-count assertions in tests
- [ ] `L3` `WHERE id IN (…10,000 ids…)`: problems and alternatives. ↳ = ANY($1::bigint[]), join a VALUES list or temp table
- [ ] `L3` Summary tables vs materialized views vs a data warehouse for dashboards: how do you choose?
- [ ] `L3` Async SQLAlchemy / asyncpg under load: what changes about connection usage?

## 9.9 MVCC — tuple versions, xmin/xmax, snapshots
**Learn:** DDIA ch7 "Implementing snapshot isolation" + "Visibility rules" (pdf p252–254) · https://www.postgresql.org/docs/current/mvcc-intro.html · *The Internals of PostgreSQL* ch5 "Concurrency Control" (https://www.interdb.jp/pg/)
- [ ] `L1` What is MVCC, in one sentence?
- [ ] `L1` What does "readers don't block writers, writers don't block readers" mean in Postgres?
- [ ] `L1` What are the `xmin` and `xmax` system columns on a row?
- [ ] `L2` What physically happens on an `UPDATE`? ↳ new tuple version written; old version gets xmax; indexes may get entries
- [ ] `L2` What physically happens on a `DELETE`? Is the space freed?
- [ ] `L2` What is a snapshot, and what does it contain? ↳ xmin, xmax and the list of in-progress transaction ids
- [ ] `L2` How does Postgres decide whether a tuple version is visible to your transaction?
- [ ] `L2` What is the commit log (`pg_xact`, CLOG) used for?
- [ ] `L2` What are hint bits, and why can a plain `SELECT` cause disk writes? ↳ first reader sets hint bits and dirties the page
- [ ] `L2` What is the visibility map, and what uses it? ↳ index-only scans and VACUUM skipping all-visible pages
- [ ] `L2` Postgres vs MySQL InnoDB: where do old row versions live? ↳ Postgres in the table heap; InnoDB in undo logs
- [ ] `L2` Why does an update-heavy table grow on disk while its row count stays flat?
- [ ] `L3` What is a dead tuple, and who might still need it? ↳ older snapshots: long transactions, replication slots, standby feedback
- [ ] `L3` Why does one long-running transaction cause bloat in every table of the database? ↳ holds back the global xmin horizon
- [ ] `L3` What is a subtransaction (SAVEPOINT), and why can heavy use slow Postgres down? ↳ subxid cache overflow (64 per backend), SLRU contention
- [ ] `L3` What is a MultiXact, and when does Postgres create one? ↳ several transactions lock one row, e.g. FK checks, FOR SHARE
- [ ] `L3` Updating a non-indexed column still adds entries to every index. When, and why? ↳ non-HOT update when the page has no room
- [ ] `L3` What is TOAST, and how does it interact with updates to large values?

## 9.10 VACUUM, autovacuum, bloat and transaction ID wraparound
**Learn:** DBI ch4 "Vacuum and Maintenance" (pdf p134–138) · https://www.postgresql.org/docs/current/routine-vacuuming.html · https://www.postgresql.org/docs/current/runtime-config-autovacuum.html · https://github.com/reorg/pg_repack
- [ ] `L1` What does VACUUM do?
- [ ] `L1` VACUUM vs VACUUM FULL. ↳ FULL rewrites the table under an ACCESS EXCLUSIVE lock
- [ ] `L1` What is table bloat? What is index bloat?
- [ ] `L1` What is autovacuum?
- [ ] `L2` When does autovacuum start on a table? ↳ dead tuples > threshold + scale_factor × table rows
- [ ] `L2` Why is the default `autovacuum_vacuum_scale_factor = 0.2` bad for a 500M-row table? What do you set? ↳ waits for 100M dead rows; lower it per table
- [ ] `L2` Autovacuum can't keep up. Which settings do you change? ↳ cost_limit/cost_delay, more workers, per-table settings, maintenance_work_mem
- [ ] `L2` How do you measure bloat? ↳ n_dead_tup in pg_stat_user_tables, pgstattuple, estimate queries
- [ ] `L2` How do you remove bloat without locking the table for hours? ↳ pg_repack or pg_squeeze; REINDEX CONCURRENTLY for indexes
- [ ] `L2` Does VACUUM give disk space back to the operating system? ↳ only empty pages at the end; otherwise reused
- [ ] `L2` What is transaction ID wraparound? Why are 32-bit xids a problem? ↳ ~2 billion usable ids; old rows would look like future rows
- [ ] `L2` What is freezing, and what does `VACUUM FREEZE` do?
- [ ] `L2` What happens if you ignore wraparound warnings? ↳ Postgres stops assigning xids and refuses writes
- [ ] `L2` What is an anti-wraparound autovacuum, and why shouldn't you keep cancelling it?
- [ ] `L3` Name four things that stop VACUUM from removing dead tuples. ↳ long or idle-in-transaction sessions, stale slots, prepared transactions, standby feedback
- [ ] `L3` `age(datfrozenxid)` is at 1.5 billion. Walk me through what you do right now.
- [ ] `L3` A queue-like table (insert, update, delete all day) is bloated and slow. Fix it. ↳ aggressive per-table autovacuum, fillfactor, short transactions, partition and drop
- [ ] `L3` Why do mass DELETEs hurt more than dropping a partition or TRUNCATE?
- [ ] `L3` Why vacuum an insert-only table at all? ↳ sets visibility map, freezes rows; PG13 added insert-triggered autovacuum

## 9.11 Transactions, isolation levels and anomalies
**Learn:** DDIA ch7 "The meaning of ACID" (pdf p237–241) · DDIA ch7 "Weak isolation levels" (pdf p246–264) · DDIA ch7 "Serializable snapshot isolation (SSI)" (pdf p274–279) · DBI ch5 "Read and Write Anomalies" + "Isolation Levels" (pdf p170–173) · https://www.postgresql.org/docs/current/transaction-iso.html · https://wiki.postgresql.org/wiki/SSI
- [ ] `L1` What does ACID stand for? What does each letter really mean?
- [ ] `L1` Name the four SQL isolation levels.
- [ ] `L1` What is the default isolation level in Postgres? ↳ read committed
- [ ] `L1` Define dirty read, non-repeatable read and phantom read.
- [ ] `L2` Define lost update and write skew, with an example of each. ↳ two concurrent increments; two doctors both go off call
- [ ] `L2` Read committed vs repeatable read in Postgres: what does each statement see? ↳ RC: new snapshot per statement; RR: one per transaction
- [ ] `L2` Does Postgres support read uncommitted? ↳ accepted, but behaves as read committed
- [ ] `L2` The SQL standard allows phantoms at repeatable read. Why doesn't Postgres show them? ↳ its repeatable read is snapshot isolation
- [ ] `L2` At repeatable read, two transactions update the same row. What happens to the second one? ↳ serialization failure error after the first commits; retry
- [ ] `L2` How do you prevent a lost update on a counter? Give three ways. ↳ atomic SET x = x + 1, SELECT FOR UPDATE, version-column compare-and-set
- [ ] `L2` Optimistic concurrency with a `version` column: write the UPDATE and explain the retry.
- [ ] `L2` Two users book the last seat at the same moment. How do you prevent double booking? ↳ row lock, conditional UPDATE, unique constraint, or serializable
- [ ] `L2` Give a write-skew example that repeatable read in Postgres does NOT prevent.
- [ ] `L2` How does serializable (SSI) work in Postgres? ↳ tracks read-write dependencies with SIRead locks; aborts dangerous cycles
- [ ] `L2` Why must an app using serializable have a retry loop? Which SQLSTATE codes do you retry? ↳ 40001 serialization_failure; 40P01 deadlock_detected
- [ ] `L2` What does serializable cost in Postgres?
- [ ] `L2` What is autocommit? What happens when your driver silently opens a transaction and never commits?
- [ ] `L3` Why can't `SELECT … FOR UPDATE` stop write skew when the conflicting row doesn't exist yet? ↳ phantom: nothing to lock; materialize conflicts or serializable
- [ ] `L3` What does "materializing conflicts" mean? Give an example.
- [ ] `L3` Snapshot isolation vs true serializability: show an anomaly that snapshot isolation allows.
- [ ] `L3` What does `PREPARE TRANSACTION` (two-phase commit) do, and why avoid 2PC across services?
- [ ] `L3` What are `SERIALIZABLE READ ONLY DEFERRABLE` transactions for?
- [ ] `L3` A transaction calls an external API for 5 seconds between two statements. What problems does that cause?

## 9.12 Locking, job queues, advisory locks and deadlocks
**Learn:** DDIA ch7 "Explicit locking" (pdf p257–258) · DBI ch5 "Deadlocks" (pdf p179–180) · https://www.postgresql.org/docs/current/explicit-locking.html · https://www.postgresql.org/docs/current/sql-select.html ("The Locking Clause") · https://www.crunchydata.com/blog/message-queuing-using-native-postgresql
- [ ] `L1` Row-level locks vs table-level locks.
- [ ] `L1` What does `SELECT … FOR UPDATE` do?
- [ ] `L1` What is a deadlock?
- [ ] `L2` `FOR UPDATE` vs `FOR NO KEY UPDATE` vs `FOR SHARE` vs `FOR KEY SHARE`. ↳ FK checks take KEY SHARE; NO KEY UPDATE doesn't block them
- [ ] `L2` `NOWAIT` vs `SKIP LOCKED`: what does each do and when do you use it?
- [ ] `L2` How do you implement a job queue in Postgres? ↳ SELECT … FOR UPDATE SKIP LOCKED LIMIT n, mark taken, commit
- [ ] `L2` Postgres as a queue vs Redis vs RabbitMQ/Kafka: when is Postgres enough?
- [ ] `L2` Why can an "instant" `ALTER TABLE ADD COLUMN` freeze the whole app? ↳ ACCESS EXCLUSIVE waits behind a long query; all new queries queue behind it
- [ ] `L2` What is `lock_timeout`, and why set it on every migration?
- [ ] `L2` How does Postgres detect deadlocks? What is `deadlock_timeout`?
- [ ] `L2` Two transactions update rows A and B in opposite order. Fix it. ↳ consistent lock order, e.g. ORDER BY id FOR UPDATE
- [ ] `L2` How do you see who is blocking whom? ↳ pg_blocking_pids(), pg_locks joined with pg_stat_activity
- [ ] `L2` What are advisory locks? Session-level vs transaction-level. ↳ app-chosen lock ids; xact locks release at commit
- [ ] `L2` Use an advisory lock so only one instance runs a cron job. What breaks behind PgBouncer transaction mode? ↳ session locks leak across clients; use xact locks
- [ ] `L2` Postgres advisory lock vs Redis `SET NX` lock: which is safer, and why?
- [ ] `L2` Does inserting a child row lock the parent row? ↳ yes, FOR KEY SHARE on the referenced row
- [ ] `L3` Which table lock modes exist, and which one blocks a plain `SELECT`? ↳ only ACCESS EXCLUSIVE
- [ ] `L3` Why does a concurrent `UPDATE … WHERE id IN (subquery)` without ordering deadlock?
- [ ] `L3` A SKIP LOCKED worker crashes mid-job. What happens to the row? How do you handle jobs that hang? ↳ lock released on disconnect; lease/visible_after column
- [ ] `L3` How does `LISTEN/NOTIFY` help a Postgres queue, and what are its limits? ↳ not durable, 8000-byte payload, needs a session connection
- [ ] `L3` In read committed, the row you `SELECT … FOR UPDATE` changed while you waited. What does Postgres do? ↳ re-checks WHERE on the newest version (EvalPlanQual)
- [ ] `L3` Many sessions update one hot counter row. What happens, and how do you redesign it? ↳ lock contention; sharded counter rows, batched increments

## 9.13 Connections, pooling and memory settings
**Learn:** DBI ch5 "Buffer Management" (pdf p144–156) · https://www.pgbouncer.org/features.html · https://www.postgresql.org/docs/current/runtime-config-connection.html · https://www.postgresql.org/docs/current/runtime-config-resource.html · https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server
- [ ] `L1` Why does Postgres need a connection pooler? ↳ one OS process per connection: memory, fork cost, contention
- [ ] `L1` What is PgBouncer?
- [ ] `L1` What is `max_connections`, and what is its default? ↳ 100
- [ ] `L2` PgBouncer session vs transaction vs statement pooling.
- [ ] `L2` What breaks in transaction pooling mode? ↳ session state: SET, temp tables, session advisory locks, LISTEN
- [ ] `L2` Prepared statements behind PgBouncer: what was the problem, and what did PgBouncer 1.21 change? ↳ now tracks protocol-level prepared statements (max_prepared_statements)
- [ ] `L2` How do you size a connection pool? ↳ start near cores × 2; measure; small pools usually beat big ones
- [ ] `L2` 10 pods × 20 connections × 3 services hit one database. What goes wrong at deploy time?
- [ ] `L2` App-side pool (SQLAlchemy, HikariCP, Prisma) vs PgBouncer vs both.
- [ ] `L2` The pool is exhausted. What do users see, and how do you notice? ↳ waits then pool timeout errors; pool metrics, pg_stat_activity
- [ ] `L2` What is "idle in transaction", and why is it dangerous? Which timeout fixes it? ↳ holds locks and xmin; idle_in_transaction_session_timeout
- [ ] `L2` `statement_timeout`: where do you set it (role, database, session) and why?
- [ ] `L2` What is `shared_buffers`, and what is a typical starting value? ↳ about 25% of RAM; OS page cache does the rest
- [ ] `L2` What is `work_mem`, and why is setting it to 1 GB dangerous? ↳ per sort/hash node, per query, times connections
- [ ] `L2` What do `maintenance_work_mem` and `effective_cache_size` do? ↳ effective_cache_size is only a planner hint; allocates nothing
- [ ] `L2` Postgres double-buffers through `shared_buffers` and the OS page cache. Why does that matter for sizing?
- [ ] `L3` Serverless functions (Lambda) hitting Postgres directly: what goes wrong and how do you fix it? ↳ connection storms; RDS Proxy, PgBouncer, HTTP data APIs
- [ ] `L3` Why does throughput fall when active connections go from 100 to 1000? ↳ context switches, lock contention, snapshot cost, cache thrashing
- [ ] `L3` PgBouncer is single-threaded. How do you scale it? ↳ several instances with so_reuseport; or PgCat, Supavisor, Odyssey
- [ ] `L3` Why enable huge pages for a large `shared_buffers`?
- [ ] `L3` Where do connection leaks come from in async Python apps, and how do you catch them?

## 9.14 WAL, checkpoints, crash recovery, backups and PITR
**Learn:** DBI ch5 "Recovery" (pdf p157–165) · DDIA ch3 "B-trees" (pdf p102, making B-trees reliable) · https://www.postgresql.org/docs/current/wal-intro.html · https://www.postgresql.org/docs/current/continuous-archiving.html · https://www.postgresql.org/docs/current/backup-dump.html · https://pgbackrest.org
- [ ] `L1` What is the write-ahead log (WAL), and why does it exist?
- [ ] `L1` What does "durable" mean when `COMMIT` returns? ↳ the commit's WAL record is flushed to disk first
- [ ] `L1` Logical backup (`pg_dump`) vs physical backup (`pg_basebackup`).
- [ ] `L1` What is point-in-time recovery (PITR)?
- [ ] `L2` Walk through crash recovery after a power cut. ↳ replay WAL from the last checkpoint's redo point
- [ ] `L2` What is a checkpoint? What do `checkpoint_timeout` and `max_wal_size` control?
- [ ] `L2` Why do too-frequent checkpoints hurt write performance? ↳ more full-page writes inflate WAL; I/O spikes
- [ ] `L2` What are full-page writes, and what problem do they solve? ↳ torn 8 KB pages after a partial write
- [ ] `L2` What does `synchronous_commit = off` trade away? ↳ may lose the last few hundred ms of commits; no corruption
- [ ] `L2` Why is `fsync = off` never acceptable in production?
- [ ] `L2` How does PITR work end to end? ↳ base backup + archived WAL + recovery_target_time
- [ ] `L2` Someone ran `DELETE FROM orders` with no `WHERE` in prod. How do you recover? ↳ PITR to a new instance just before; copy rows back
- [ ] `L2` Which backup tools would you use in production? ↳ pgBackRest, WAL-G, Barman, managed snapshots
- [ ] `L2` Define RPO and RTO. What numbers does your backup setup give?
- [ ] `L2` How do you know your backups actually work? ↳ scheduled automated restore tests
- [ ] `L3` What are the `wal_level` values (minimal, replica, logical), and what needs each?
- [ ] `L3` The WAL disk fills up. What are the usual causes? ↳ failing archive_command, inactive replication slot, huge max_wal_size
- [ ] `L3` Why is `pg_dump` consistent while writes continue? ↳ it runs inside one repeatable read snapshot
- [ ] `L3` How does group commit (`commit_delay`) share one fsync among many transactions?
- [ ] `L3` How does the WAL tie together crash recovery, streaming replication and logical decoding?

## 9.15 Replication, failover and high availability
**Learn:** DDIA ch5 "Leaders and Followers" (pdf p168–177) · DDIA ch5 "Problems With Replication Lag" (pdf p177–183) · https://www.postgresql.org/docs/current/warm-standby.html · https://www.postgresql.org/docs/current/logical-replication.html · https://patroni.readthedocs.io
- [ ] `L1` What is streaming (physical) replication?
- [ ] `L1` What is a read replica (hot standby)?
- [ ] `L1` Synchronous vs asynchronous replication.
- [ ] `L2` Streaming vs logical replication: what is copied, and when do you use each? ↳ physical: whole cluster, same version; logical: row changes per table
- [ ] `L2` What is replication lag, and how do you measure it? ↳ pg_stat_replication write/flush/replay_lag; LSN difference
- [ ] `L2` A user updates their profile, refreshes, and sees the old value. Why, and how do you fix it? ↳ read-your-writes: read from primary briefly, or wait for LSN
- [ ] `L2` What is a replication slot, and how can an abandoned one take down the primary? ↳ WAL retained forever until the disk fills
- [ ] `L2` With synchronous replication, what do `remote_write`, `on` and `remote_apply` mean?
- [ ] `L2` The only synchronous standby dies. What happens to writes on the primary? ↳ commits hang; use quorum ANY 1 (s1, s2)
- [ ] `L2` What does `hot_standby_feedback` do, and what is the trade-off? ↳ fewer query cancels on replica vs bloat on primary
- [ ] `L2` A replica query fails with "canceling statement due to conflict with recovery". Why?
- [ ] `L2` How does automatic failover work with Patroni? ↳ leader key with TTL in etcd/Consul; replica promoted; old primary demoted
- [ ] `L2` What is split-brain, and how does a Postgres HA setup prevent it?
- [ ] `L2` What does `pg_rewind` do?
- [ ] `L2` After failover, how does the app find the new primary? ↳ DNS/VIP, HAProxy with health checks, target_session_attrs in libpq
- [ ] `L3` With asynchronous replication, what data can a failover lose, and how do you bound it?
- [ ] `L3` Zero-downtime major-version upgrade with logical replication: walk through the steps.
- [ ] `L3` What does logical replication not copy? ↳ DDL, sequence values, large objects; schema must pre-exist on subscriber
- [ ] `L3` Managed HA (RDS Multi-AZ, Aurora, Azure Flexible Server, Cloud SQL): how is Aurora's storage different?
- [ ] `L3` Why keep a delayed replica 1 hour behind (`recovery_min_apply_delay`)?

## 9.16 Partitioning, sharding and scaling reads and writes
**Learn:** DDIA ch6 "Partitioning by key range" + "by hash of key" (pdf p216–218) · DDIA ch6 "Skewed workloads and relieving hot spots" + "Partitioning and secondary indexes" (pdf p218–223) · DDIA ch6 "Rebalancing partitions" (pdf p223–227) · https://www.postgresql.org/docs/current/ddl-partitioning.html · https://docs.citusdata.com · https://www.notion.com/blog/sharding-postgres-at-notion
- [ ] `L1` Partitioning vs sharding.
- [ ] `L1` Range vs list vs hash partitioning in Postgres: one use each.
- [ ] `L1` Vertical vs horizontal scaling.
- [ ] `L2` What is partition pruning, and when does it fail? ↳ needs partition key in WHERE; casts or functions on the key break it
- [ ] `L2` What do you gain by partitioning a 2 TB events table by month? ↳ pruning, instant drop of old data, smaller indexes, per-partition vacuum
- [ ] `L2` What are the limits of declarative partitioning? ↳ unique keys must include partition key; many partitions slow planning
- [ ] `L2` How do you turn an existing large table into a partitioned one without downtime?
- [ ] `L2` How do you create future partitions automatically? ↳ pg_partman or a scheduled job; watch the default partition
- [ ] `L2` How do you scale reads in Postgres? ↳ replicas, caching, materialized views, read routing
- [ ] `L2` How do you scale writes in Postgres? ↳ batching, fewer indexes, partitioning, bigger machine, then sharding
- [ ] `L2` What is Citus? Distributed tables vs reference tables. ↳ coordinator + workers; distribution column; co-located joins
- [ ] `L2` Pick a shard key for a multi-tenant SaaS, and for a chat app. ↳ tenant_id; conversation_id keeps a chat's messages together
- [ ] `L2` What breaks when you shard: joins, transactions, unique constraints, sequences? How do you handle each?
- [ ] `L2` Your Postgres is at 90% CPU. What do you check, in order? ↳ pg_stat_statements by total time, missing indexes, connections, vacuum, then scale
- [ ] `L3` How did Instagram, Notion or Figma shard Postgres, and what did they do about ids?
- [ ] `L3` Move one hot tenant to its own shard with no downtime.
- [ ] `L3` Why create many small logical shards on a few physical hosts?
- [ ] `L3` What signs tell you single-node Postgres is no longer enough, and what do you try first?
- [ ] `L3` Distributed SQL (CockroachDB, YugabyteDB, Spanner) vs Citus vs sharding in the application.

## 9.17 Migrations without downtime
**Learn:** DDIA ch4 "Data flow through databases" (pdf p147–149) · https://gocardless.com/blog/zero-downtime-postgres-migrations-the-hard-parts/ · https://www.postgresql.org/docs/current/sql-createindex.html ("Building Indexes Concurrently") · https://planetscale.com/blog/backward-compatible-databases-changes · https://alembic.sqlalchemy.org/en/latest/autogenerate.html
- [ ] `L1` What is a schema migration? Which tools have you used? ↳ Alembic, Prisma Migrate, TypeORM, Django migrations
- [ ] `L1` What is expand → migrate → contract?
- [ ] `L2` Adding a nullable column to a 100M-row table: fast or slow? A column with a constant default? ↳ both metadata-only since PG11; volatile default rewrites
- [ ] `L2` Add a NOT NULL column to a 100M-row table without downtime. ↳ nullable, backfill in batches, CHECK NOT VALID, VALIDATE, SET NOT NULL
- [ ] `L2` How do you add an index to a busy table? ↳ CREATE INDEX CONCURRENTLY, outside a transaction block
- [ ] `L2` `CREATE INDEX CONCURRENTLY` failed halfway. What state is the table in? ↳ an INVALID index remains; drop it and retry
- [ ] `L2` Add a foreign key to a big table without blocking writes. ↳ ADD CONSTRAINT … NOT VALID, then VALIDATE CONSTRAINT
- [ ] `L2` Rename a column a live app uses. ↳ add new, dual-write, backfill, switch reads, drop old
- [ ] `L2` Change a column from `int` to `bigint` on a huge table. Why is it hard, and how do you do it? ↳ full rewrite under lock; new column, trigger, backfill, swap
- [ ] `L2` Backfill 50M rows safely. ↳ batches by primary key, pauses, watch replica lag, idempotent
- [ ] `L2` Why must code and schema stay backward compatible across a deploy?
- [ ] `L2` How do you drop a column safely? ↳ stop reading it in code first; ORMs that select every column
- [ ] `L2` Why should each migration set `lock_timeout` and be retried?
- [ ] `L2` What does Alembic autogenerate miss or get wrong? ↳ renames seen as drop + add, server defaults, some type changes
- [ ] `L3` An `int` primary key is about to hit 2^31. What do you do under time pressure?
- [ ] `L3` How do you test a migration against production-sized data first?
- [ ] `L3` Major upgrade (14 → 17): `pg_upgrade --link` vs logical replication vs dump and restore.
- [ ] `L3` How do you roll back a migration that already ran a destructive step?
- [ ] `L3` MySQL needs gh-ost and pt-osc for online changes. Why does Postgres need them less?

## 9.18 JSONB, full-text search and pgvector
**Learn:** DDIA ch2 "Relational vs. document databases today" (pdf p60–63) · AIE ch6 "Retrieval Algorithms" (pdf p283–290) · https://www.postgresql.org/docs/current/datatype-json.html · https://www.postgresql.org/docs/current/textsearch-intro.html · https://github.com/pgvector/pgvector
- [ ] `L1` `json` vs `jsonb`.
- [ ] `L1` What do `->`, `->>` and `@>` do on JSONB?
- [ ] `L1` What are `tsvector` and `tsquery`?
- [ ] `L1` What is pgvector?
- [ ] `L2` JSONB column vs real columns: when is JSONB fine, and when does it hurt? ↳ no planner stats, no types or constraints, whole value rewritten
- [ ] `L2` How do you index a JSONB field you filter on often? ↳ GIN for containment; B-tree expression index on (data->>'key')
- [ ] `L2` What does updating one key inside a 1 MB JSONB value cost? ↳ new tuple version, TOAST rewrite, WAL for the whole value
- [ ] `L2` How do you validate the shape of JSONB data? ↳ CHECK with jsonb_typeof, generated columns, schema in the app
- [ ] `L2` Search over a 1M-row product catalogue: Postgres full-text or Elasticsearch? ↳ start with Postgres FTS + trigram; ES for relevance tuning, facets
- [ ] `L2` How does an inverted index work, and how is a GIN index one?
- [ ] `L2` How does Postgres full-text search work? ↳ parser, dictionaries, stemming, stop words, ts_rank
- [ ] `L2` How do you keep a `tsvector` up to date? ↳ stored generated column plus a GIN index
- [ ] `L2` Typo-tolerant search and autocomplete in Postgres. ↳ pg_trgm similarity; prefix tsquery with :*
- [ ] `L2` pgvector HNSW vs IVFFlat: build time, recall, memory, updates. ↳ HNSW: better recall, slower build; IVFFlat needs data before building
- [ ] `L2` Vector search filtered by `user_id`: what goes wrong with an HNSW index plus WHERE? ↳ post-filtering returns too few rows; iterative scans, partial indexes
- [ ] `L2` pgvector vs Qdrant: when is pgvector enough? ↳ few million vectors, need joins and transactions; Qdrant for heavy filtering, scale
- [ ] `L2` Hybrid search in Postgres: combine full-text rank and vector similarity. ↳ run both, merge with reciprocal rank fusion
- [ ] `L3` You move search to Elasticsearch. How do you keep it in sync with Postgres? ↳ outbox or CDC (Debezium), idempotent indexer, full reindex path
- [ ] `L3` How do generated columns help a JSONB-heavy schema?
- [ ] `L3` pgvector operators `<->`, `<#>`, `<=>`: what does each compute, and why must the index opclass match? ↳ L2, negative inner product, cosine distance
- [ ] `L3` What are `halfvec` and binary quantization in pgvector for?

## 9.19 Monitoring, tuning and pgbench
**Learn:** https://www.postgresql.org/docs/current/monitoring-stats.html · https://www.postgresql.org/docs/current/pgstatstatements.html · https://www.postgresql.org/docs/current/runtime-config-logging.html · https://www.postgresql.org/docs/current/pgbench.html · https://www.postgresql.org/docs/current/auto-explain.html
- [ ] `L1` What is `pg_stat_statements`?
- [ ] `L1` What is `pg_stat_activity`?
- [ ] `L1` How do you log slow queries in Postgres? ↳ log_min_duration_statement
- [ ] `L2` Which `pg_stat_statements` column do you sort by first, and why total time before mean time?
- [ ] `L2` What do `wait_event_type` and `wait_event` in `pg_stat_activity` tell you?
- [ ] `L2` What goes on a Postgres dashboard? ↳ connections, TPS, p95 latency, cache hit ratio, replica lag, dead tuples, locks, disk
- [ ] `L2` What is the buffer cache hit ratio, and what value worries you?
- [ ] `L2` How do you find tables that get many sequential scans? ↳ seq_scan and seq_tup_read in pg_stat_user_tables
- [ ] `L2` `pg_cancel_backend` vs `pg_terminate_backend`.
- [ ] `L2` What is pgbench, and how do you run a benchmark that means something? ↳ scale factor, clients, threads, duration, custom scripts, warm cache
- [ ] `L2` You raise `shared_buffers` from 128 MB to 8 GB. How do you prove it helped?
- [ ] `L2` Which settings do you change first on a fresh install? ↳ shared_buffers, effective_cache_size, work_mem, maintenance_work_mem, max_wal_size, random_page_cost
- [ ] `L2` What do `log_lock_waits` and `log_temp_files` log?
- [ ] `L3` How do you find the queries that cause the most disk I/O? ↳ shared_blks_read and temp_blks_written in pg_stat_statements
- [ ] `L3` What does `track_io_timing` add to plans and statistics?
- [ ] `L3` A load test shows p99 spikes every 5 minutes. What is your hypothesis? ↳ checkpoints, autovacuum, cron jobs; check logs and checkpoint stats
- [ ] `L3` Why are pgbench numbers from a laptop misleading for production?
- [ ] `L3` pganalyze, pgBadger, PMM, Datadog DBM: what does each add over the built-in views?

## 9.20 Postgres vs MySQL vs MongoDB vs DynamoDB
**Learn:** DDIA ch2 "Relational Model vs. Document Model" (pdf p48–63) · DDIA ch6 "Partitioning secondary indexes by term" (pdf p222–223) · https://www.mongodb.com/docs/manual/data-modeling/ · https://www.mongodb.com/docs/manual/aggregation/ · https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html
- [ ] `L1` SQL vs NoSQL: what are the real differences, beyond "schema"?
- [ ] `L1` What is a document database?
- [ ] `L1` What are MongoDB's equivalents of a table, a row and a join? ↳ collection, document, $lookup
- [ ] `L2` When would you pick MongoDB over Postgres? When would you not?
- [ ] `L2` Embed or reference comments in a blog-post document? ↳ unbounded growth means reference; 16 MB document limit
- [ ] `L2` You run both Postgres and MongoDB in production. Which data went where, and why?
- [ ] `L2` MongoDB multi-document transactions: since when, and what do they cost vs Postgres? ↳ replica sets since 4.0, sharded clusters since 4.2
- [ ] `L2` MongoDB indexes vs Postgres indexes: compound-index prefix rule, multikey indexes on arrays.
- [ ] `L2` MongoDB aggregation pipeline vs SQL GROUP BY and window functions.
- [ ] `L2` MongoDB write concern and read concern: what do `w: "majority"` and `readConcern: "majority"` give you?
- [ ] `L2` Postgres JSONB vs MongoDB for flexible-schema data: what does each do better?
- [ ] `L2` Postgres vs MySQL (InnoDB): MVCC, clustered index, replication, features you'd miss.
- [ ] `L2` DynamoDB: partition key, sort key, GSIs, single-table design. When does it beat Postgres?
- [ ] `L2` In DynamoDB you design for access patterns first. What hurts when a new query arrives later?
- [ ] `L2` "Schemaless" in MongoDB: where does the schema actually live? ↳ in application code and every reader: schema-on-read
- [ ] `L2` Postgres vs MongoDB for a chat app's message history.
- [ ] `L3` MongoDB sharding: shard key choice, chunks, the balancer, jumbo chunks, scatter-gather queries.
- [ ] `L3` MongoDB replica-set election vs Patroni failover: what happens to in-flight writes? ↳ w:1 writes can roll back; majority writes survive
- [ ] `L3` Cassandra or ScyllaDB for write-heavy time series vs partitioned Postgres or TimescaleDB.
- [ ] `L3` Plan a migration from MongoDB to Postgres (or back) with no downtime. ↳ CDC or dual-write, backfill, verify, switch reads, then writes
- [ ] `L3` Why do teams end up with "Postgres for everything" (queues, search, vectors, JSON)? Where does it break?
- [ ] `L3` Why are column stores (ClickHouse, BigQuery, Redshift) fast for analytics, and when do reports move there?

## 9.21 Debug this slow query — scenarios
**Learn:** DDIA ch3 "Aggregation: Data cubes and materialized views" (pdf p120–122) · https://www.postgresql.org/docs/current/using-explain.html · https://use-the-index-luke.com · https://explain.dalibo.com
### Scenarios
- [ ] `L2` An endpoint went from 50 ms to 4 s after a big data import. No code changed. Where do you start? ↳ stale statistics: ANALYZE, then compare plans
- [ ] `L2` A query is fast in staging and slow in prod. What differences do you check? ↳ data size and skew, stats, settings, cache, concurrency, plan
- [ ] `L2` A plan shows Seq Scan on 40M rows with `Rows Removed by Filter: 39999990`. Fix it.
- [ ] `L2` A plan shows a nested loop with 2 million loops of an inner index scan. What went wrong? ↳ outer side row count badly underestimated
- [ ] `L2` The same query takes 20 ms sometimes and 9 s other times. What do you suspect? ↳ lock waits, cold cache, generic plan, parameter skew, checkpoints
- [ ] `L2` A single-row `UPDATE` by primary key takes 30 s. Why? ↳ waiting on a row lock; check pg_locks
- [ ] `L2` Dashboard reports are slowing down the production database. What do you do? ↳ replica, rollup tables or materialized views, then a warehouse
- [ ] `L2` Page 1 of a list API is fast; page 5000 is slow. Fix it.
- [ ] `L2` `ILIKE '%term%'` over 5M rows is slow. What are your options?
- [ ] `L2` The COUNT(*) for "total pages" is slower than fetching the page itself. What do you do?
- [ ] `L2` An ORM query joins 7 tables and selects 120 columns for a list view. Fix it without rewriting the app.
- [ ] `L3` A query got slow right after a Postgres major upgrade. Why, and how do you check? ↳ planner stats not carried over: run ANALYZE; compare plans
- [ ] `L3` Disk I/O is at 100%, CPU is low, and queries crawl. Walk through your investigation.
- [ ] `L3` A nightly DELETE of old rows runs for hours and slows everything. Redesign it. ↳ partition by time and drop partitions; or small batches
- [ ] `L3` A hash join spills to disk in 64 batches. What are your options? ↳ more work_mem for that query, fewer columns, earlier filters
### Your Jigsaw report: 12 min → 30 s
- [ ] `L2` Walk me through the report that took 12 minutes. What did it compute, and where did the time go?
- [ ] `L2` How did you find the bottleneck: EXPLAIN, query logs, profiling the app, or counting queries?
- [ ] `L2` Was it N+1 queries, missing indexes, aggregation in app code, or something else? Show before and after.
- [ ] `L2` Did you move aggregation into SQL? Which GROUP BY or window functions did you use?
- [ ] `L2` Which indexes did you add, with which column order, and why that order?
- [ ] `L3` Why 30 s and not 1 s? What would it take to make it sub-second? ↳ pre-aggregation, materialized views, incremental rollups, caching
- [ ] `L3` How did you check that the fast report returned exactly the same numbers as the old one?
- [ ] `L3` Did the fix add load to the primary? Would you move it to a replica or run it as a background job?
- [ ] `L3` If the data grew 100×, which part of your fix breaks first?
- [ ] `L3` Precompute the report (materialized view or summary table) or compute it live? Trade-offs.

## 9.22 Rapid-fire round
- [ ] `L1` Default Postgres port? ↳ 5432
- [ ] `L1` Default Postgres page (block) size? ↳ 8 KB
- [ ] `L1` Which isolation level do you get if you don't choose one?
- [ ] `L1` What does MVCC stand for?
- [ ] `L1` What does WAL stand for?
- [ ] `L1` Which index type serves JSONB `@>` queries?
- [ ] `L1` Which index type suits a huge append-only table filtered by time?
- [ ] `L1` What does `INCLUDE` add to `CREATE INDEX`?
- [ ] `L1` What does `SKIP LOCKED` skip?
- [ ] `L1` Can you run `CREATE INDEX CONCURRENTLY` inside `BEGIN … COMMIT`?
- [ ] `L1` Which PgBouncer pool mode do most web apps use?
- [ ] `L1` What must exist for `ON CONFLICT (email)` to work?
- [ ] `L1` RANK vs DENSE_RANK in one line.
- [ ] `L1` Partial index in one line.
- [ ] `L1` Materialized view vs view in one line.
- [ ] `L1` Which view shows currently running queries?
- [ ] `L1` Which extension shows the most expensive queries over time?
- [ ] `L1` Physical vs logical replication in one line.
- [ ] `L1` What is TOAST?
- [ ] `L1` Why is xid wraparound dangerous, in one line?
- [ ] `L1` Which should you store, `timestamp` or `timestamptz`?
- [ ] `L1` What does the `ANALYZE` command update?
- [ ] `L1` OFFSET vs keyset pagination in one line.
- [ ] `L1` Is `work_mem` per connection, per query, or per operation?
- [ ] `L1` What is Patroni for?
- [ ] `L1` What does Citus add to Postgres?
- [ ] `L1` What does an index-only scan avoid reading?
- [ ] `L1` Which lock mode does `VACUUM FULL` take?
- [ ] `L1` What is MongoDB's maximum document size?
