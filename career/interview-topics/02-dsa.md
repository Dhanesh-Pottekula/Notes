# 2. Data structures and algorithms (P0)

Target for 3 years: LeetCode **mediums in ≤25 min**, explain the brute force first, then optimise, state time and
space Big-O, and dry-run on an example. Do NC150 in order (about 2 problems a day ≈ 12 weeks), then redo the ones
you failed.

**How to practise each problem:** 5 min think → code → test edge cases (empty, one element, duplicates,
negatives, overflow) → say complexity. If stuck at 25 min, watch the NeetCode video, then redo it 3 days later.

**Learn (all sections):** NC150 (neetcode.io, free videos) · LC · *Grokking the Coding Interview* patterns
(free summaries online) · visualgo.net for trees/graphs/heaps.

---

## 2.1 Complexity
- [ ] Big-O, Big-Θ, Big-Ω; best/average/worst case ↳ https://www.bigocheatsheet.com · https://neetcode.io/courses (free "Algorithms & Data Structures for Beginners") · https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/
- [ ] Amortised cost (dynamic array append, hash table resize) ↳ https://en.wikipedia.org/wiki/Amortized_analysis · https://wiki.python.org/moin/TimeComplexity
- [ ] Recursion cost: recursion tree, Master theorem basics (T(n)=2T(n/2)+n → n log n) ↳ Abdul Bari "Masters Theorem" videos · https://en.wikipedia.org/wiki/Master_theorem_%28analysis_of_algorithms%29 · https://visualgo.net/en/recursion
- [ ] Space: call stack depth counts; in-place vs extra memory ↳ https://www.techinterviewhandbook.org/algorithms/recursion/ · https://visualgo.net/en/recursion
- [ ] Common orders: 1 < log n < n < n log n < n² < 2ⁿ < n!; what n each allows in ~1 s (n≤10⁸ ops) ↳ https://usaco.guide/bronze/time-comp (n limits per complexity) · https://www.bigocheatsheet.com

**Questions:** Why is appending to a dynamic array O(1) amortised? · What's the space complexity of recursive DFS?
· Why is hash map lookup "O(1)" and when is it O(n)?

## 2.2 Arrays and strings
- [ ] Indexing, in-place swaps, reversing, rotating ↳ https://leetcode.com/problems/rotate-array/ · https://leetcode.com/problems/reverse-string/ · https://www.techinterviewhandbook.org/algorithms/array/
- [ ] Prefix sums and difference arrays ↳ NeetCode "Subarray Sum Equals K" video · https://leetcode.com/problems/subarray-sum-equals-k/ · https://leetcode.com/problems/corporate-flight-bookings/ (difference array)
- [ ] Kadane's algorithm (max subarray) ↳ NeetCode "Maximum Subarray" video · https://leetcode.com/problems/maximum-subarray/ · https://en.wikipedia.org/wiki/Maximum_subarray_problem
- [ ] Sorting-based tricks; Dutch national flag (3-way partition) ↳ NeetCode "Sort Colors" video · https://leetcode.com/problems/sort-colors/ · https://en.wikipedia.org/wiki/Dutch_national_flag_problem
- [ ] String building cost (immutable strings in Python/JS), char counts with arrays of 26 ↳ https://docs.python.org/3/library/stdtypes.html#str.join · https://leetcode.com/problems/valid-anagram/ (count array of 26) · https://www.techinterviewhandbook.org/algorithms/string/
- [ ] Matrix traversal: spiral, rotate 90°, set zeroes ↳ https://leetcode.com/problems/spiral-matrix/ · https://leetcode.com/problems/rotate-image/ · https://leetcode.com/problems/set-matrix-zeroes/

**Questions (LC #):** Two Sum (1) · Best Time to Buy/Sell Stock (121) · Product of Array Except Self (238) ·
Maximum Subarray (53) · Rotate Image (48) · Spiral Matrix (54) · Subarray Sum Equals K (560) · Merge Intervals (56)

## 2.3 Hashing
- [ ] Hash map / hash set operations and costs ↳ https://wiki.python.org/moin/TimeComplexity · https://leetcode.com/problems/two-sum/ · https://leetcode.com/problems/contains-duplicate/
- [ ] How a hash table works: hash function, buckets, collisions (chaining vs open addressing), load factor, resize ↳ DDIA ch3 "Hash indexes" (pdf p92–96) · https://visualgo.net/en/hashtable · https://leetcode.com/problems/design-hashmap/
- [ ] Frequency counting, grouping by key (sorted string / count tuple) ↳ NeetCode "Group Anagrams" video · https://leetcode.com/problems/group-anagrams/ · https://leetcode.com/problems/top-k-frequent-elements/
- [ ] Using a set for O(1) membership (longest consecutive sequence) ↳ NeetCode "Longest Consecutive Sequence" video · https://leetcode.com/problems/longest-consecutive-sequence/ · DBI ch7 "Bloom Filters" (pdf p246–249)

**Questions:** Valid Anagram (242) · Group Anagrams (49) · Top K Frequent (347) · Longest Consecutive Sequence (128)
· Contains Duplicate (217) · Design a hash map from scratch (706)

## 2.4 Two pointers
- [ ] Opposite ends (sorted array, palindromes) ↳ NeetCode "Container With Most Water" video · https://leetcode.com/problems/valid-palindrome/ · https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
- [ ] Same direction (fast/slow, remove duplicates in place) ↳ https://leetcode.com/problems/remove-duplicates-from-sorted-array/ · https://leetcode.com/problems/move-zeroes/ · https://www.techinterviewhandbook.org/algorithms/array/
- [ ] 3Sum pattern (sort + fix one + two pointers) ↳ NeetCode "3Sum" video · https://leetcode.com/problems/3sum/ · https://leetcode.com/problems/trapping-rain-water/

**Questions:** Valid Palindrome (125) · Two Sum II (167) · 3Sum (15) · Container With Most Water (11) ·
Trapping Rain Water (42)

## 2.5 Sliding window
- [ ] Fixed-size window ↳ NeetCode "Permutation in String" video · https://leetcode.com/problems/maximum-average-subarray-i/ · https://leetcode.com/problems/permutation-in-string/
- [ ] Variable window: expand right, shrink left while invalid ↳ NeetCode "Longest Substring Without Repeating Characters" video · https://leetcode.com/problems/longest-substring-without-repeating-characters/ · https://leetcode.com/problems/minimum-window-substring/
- [ ] Window with a hash map of counts; "at most K distinct" ↳ NeetCode "Longest Repeating Character Replacement" video · https://leetcode.com/problems/longest-repeating-character-replacement/ · https://leetcode.com/problems/fruit-into-baskets/ (at most 2 distinct)

**Questions:** Longest Substring Without Repeating (3) · Longest Repeating Character Replacement (424) ·
Permutation in String (567) · Minimum Window Substring (76) · Sliding Window Maximum (239)

## 2.6 Stack and queue
- [ ] Stack for matching (parentheses), undo, DFS ↳ https://leetcode.com/problems/valid-parentheses/ · https://leetcode.com/problems/evaluate-reverse-polish-notation/ · https://www.techinterviewhandbook.org/algorithms/stack/
- [ ] Monotonic stack (next greater element, daily temperatures, largest rectangle) ↳ NeetCode "Daily Temperatures" video · https://leetcode.com/problems/daily-temperatures/ · https://leetcode.com/problems/largest-rectangle-in-histogram/
- [ ] Queue / deque; BFS; monotonic deque ↳ NeetCode "Sliding Window Maximum" video · https://leetcode.com/problems/sliding-window-maximum/ · https://docs.python.org/3/library/collections.html#collections.deque
- [ ] Implement a queue with two stacks; min-stack ↳ https://leetcode.com/problems/implement-queue-using-stacks/ · https://leetcode.com/problems/min-stack/ · https://cp-algorithms.com/data_structures/stack_queue_modification.html

**Questions:** Valid Parentheses (20) · Min Stack (155) · Evaluate RPN (150) · Daily Temperatures (739) ·
Car Fleet (853) · Largest Rectangle in Histogram (84) · Generate Parentheses (22)

## 2.7 Binary search
- [ ] Classic search; lower bound / upper bound; avoiding off-by-one (`lo<=hi` vs `lo<hi`) ↳ NeetCode "Binary Search" video · https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/ · DBI ch4 "Binary Search" (pdf p123–125)
- [ ] Rotated sorted array ↳ NeetCode "Search in Rotated Sorted Array" video · https://leetcode.com/problems/search-in-rotated-sorted-array/ · https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
- [ ] Binary search on the answer (min capacity, min speed) ↳ NeetCode "Koko Eating Bananas" video · https://leetcode.com/problems/koko-eating-bananas/ · https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/
- [ ] Search in 2D matrix ↳ NeetCode "Search a 2D Matrix" video · https://leetcode.com/problems/search-a-2d-matrix/

**Questions:** Binary Search (704) · Search a 2D Matrix (74) · Koko Eating Bananas (875) · Find Min in Rotated
Sorted Array (153) · Search in Rotated Sorted Array (33) · Time Based Key-Value Store (981) · Median of Two
Sorted Arrays (4)

## 2.8 Linked lists
- [ ] Reverse (iterative + recursive) ↳ NeetCode "Reverse Linked List" video · https://leetcode.com/problems/reverse-linked-list/ · https://visualgo.net/en/list
- [ ] Fast/slow pointers: middle, cycle detection (Floyd), cycle start ↳ NeetCode "Linked List Cycle" video · https://leetcode.com/problems/linked-list-cycle-ii/ · https://leetcode.com/problems/middle-of-the-linked-list/
- [ ] Merge two sorted lists; dummy head trick ↳ NeetCode "Merge Two Sorted Lists" video · https://leetcode.com/problems/merge-two-sorted-lists/ · DDIA ch3 "SSTables and LSM-trees" (pdf p96–99; merging sorted segments)
- [ ] Remove Nth from end; reorder list ↳ NeetCode "Reorder List" video · https://leetcode.com/problems/remove-nth-node-from-end-of-list/ · https://leetcode.com/problems/reorder-list/
- [ ] LRU cache = hash map + doubly linked list ↳ NeetCode "LRU Cache" video · https://leetcode.com/problems/lru-cache/ · DBI ch5 "FIFO and LRU" (pdf p151–152)

**Questions:** Reverse Linked List (206) · Merge Two Sorted Lists (21) · Linked List Cycle (141) · Reorder List
(143) · Remove Nth Node (19) · Copy List with Random Pointer (138) · Add Two Numbers (2) · LRU Cache (146) ·
Merge K Sorted Lists (23)

## 2.9 Trees
- [ ] Traversals: preorder, inorder, postorder (recursive + iterative), level order (BFS) ↳ https://visualgo.net/en/bst · https://leetcode.com/problems/binary-tree-inorder-traversal/ (do it iteratively) · https://leetcode.com/problems/binary-tree-level-order-traversal/
- [ ] Height, diameter, balanced check ↳ NeetCode "Diameter of Binary Tree" video · https://leetcode.com/problems/balanced-binary-tree/ · DBI ch2 "Tree Balancing" (pdf p59–61)
- [ ] BST property; search/insert/delete; inorder = sorted; validate BST ↳ DBI ch2 "Binary Search Trees" (pdf p57–62) · DBI ch2 "Ubiquitous B-Trees" (pdf p69–85) · https://leetcode.com/problems/validate-binary-search-tree/
- [ ] Lowest common ancestor (BST and general tree) ↳ NeetCode "Lowest Common Ancestor of a BST" video · https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/ · https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/
- [ ] Serialize / deserialize ↳ NeetCode "Serialize and Deserialize Binary Tree" video · https://leetcode.com/problems/serialize-and-deserialize-binary-tree/ · https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
- [ ] Path sums; max path sum ↳ NeetCode "Binary Tree Maximum Path Sum" video · https://leetcode.com/problems/path-sum/ · https://leetcode.com/problems/binary-tree-maximum-path-sum/

**Questions:** Invert Binary Tree (226) · Max Depth (104) · Diameter (543) · Balanced Binary Tree (110) · Same
Tree (100) · Subtree of Another Tree (572) · LCA of BST (235) · Level Order Traversal (102) · Right Side View
(199) · Validate BST (98) · Kth Smallest in BST (230) · Construct from Preorder+Inorder (105) · Max Path Sum
(124) · Serialize/Deserialize (297)

## 2.10 Heaps / priority queues
- [ ] Binary heap: array layout, sift up/down, heapify O(n) ↳ Abdul Bari "Heap - Heap Sort - Heapify - Priority Queues" video · https://visualgo.net/en/heap · https://docs.python.org/3/library/heapq.html
- [ ] Top-K with a size-K heap; K-way merge ↳ https://leetcode.com/problems/kth-largest-element-in-a-stream/ · https://leetcode.com/problems/merge-k-sorted-lists/ · DBI ch7 "Merge-Iteration" (pdf p232–236; min-heap k-way merge)
- [ ] Two heaps for running median ↳ NeetCode "Find Median from Data Stream" video · https://leetcode.com/problems/find-median-from-data-stream/
- [ ] Python `heapq` (min-heap only, negate for max); JS has none — know how to write one ↳ https://docs.python.org/3/library/heapq.html · https://leetcode.com/problems/last-stone-weight/ (max-heap by negation) · https://www.techinterviewhandbook.org/algorithms/heap/

**Questions:** Kth Largest in a Stream (703) · Last Stone Weight (1046) · K Closest Points (973) · Kth Largest
Element (215) · Task Scheduler (621) · Design Twitter (355) · Find Median from Data Stream (295)

## 2.11 Tries
- [ ] Node with children map + end flag; insert/search/startsWith ↳ NeetCode "Implement Trie (Prefix Tree)" video · https://leetcode.com/problems/implement-trie-prefix-tree/ · DDIA ch3 "Other indexing structures" (pdf p107; trie-like automaton in Lucene)
- [ ] Word search with a trie; autocomplete ↳ NeetCode "Word Search II" video · https://leetcode.com/problems/word-search-ii/ · https://leetcode.com/problems/design-add-and-search-words-data-structure/

**Questions:** Implement Trie (208) · Design Add and Search Words (211) · Word Search II (212)

## 2.12 Backtracking
- [ ] Choose → explore → un-choose template ↳ NeetCode "Subsets" video · https://leetcode.com/problems/subsets/ · https://www.techinterviewhandbook.org/algorithms/recursion/
- [ ] Subsets, permutations, combinations (with/without duplicates) ↳ https://leetcode.com/problems/permutations/ · https://leetcode.com/problems/subsets-ii/ · https://leetcode.com/problems/combination-sum-ii/
- [ ] Pruning; grid search (word search); N-Queens ↳ NeetCode "N-Queens" video · https://leetcode.com/problems/word-search/ · https://leetcode.com/problems/n-queens/

**Questions:** Subsets (78) · Combination Sum (39) · Permutations (46) · Subsets II (90) · Combination Sum II (40)
· Word Search (79) · Palindrome Partitioning (131) · Letter Combinations of a Phone Number (17) · N-Queens (51)

## 2.13 Graphs
- [ ] Representations: adjacency list vs matrix vs edge list ↳ https://visualgo.net/en/graphds · https://www.techinterviewhandbook.org/algorithms/graph/ · DDIA ch2 "Graph-like Data Models" (pdf p70–84)
- [ ] BFS (shortest path in unweighted graph), DFS (recursive + iterative) ↳ https://cp-algorithms.com/graph/breadth-first-search.html · https://cp-algorithms.com/graph/depth-first-search.html · https://visualgo.net/en/dfsbfs
- [ ] Grid as a graph: islands, flood fill, multi-source BFS (rotting oranges) ↳ NeetCode "Number of Islands" video · https://leetcode.com/problems/number-of-islands/ · https://leetcode.com/problems/rotting-oranges/
- [ ] Cycle detection (directed: colours; undirected: parent / union-find) ↳ https://cp-algorithms.com/graph/finding-cycle.html · https://leetcode.com/problems/course-schedule/ · https://leetcode.com/problems/redundant-connection/
- [ ] Topological sort: Kahn's algorithm (BFS indegree) and DFS post-order ↳ https://cp-algorithms.com/graph/topological-sort.html · NeetCode "Course Schedule II" video · https://leetcode.com/problems/course-schedule-ii/
- [ ] Union-find with path compression + union by rank ↳ https://cp-algorithms.com/data_structures/disjoint_set_union.html · William Fiset "Union Find" videos · https://visualgo.net/en/ufds
- [ ] Dijkstra (heap); when Bellman-Ford instead (negative edges) ↳ https://cp-algorithms.com/graph/dijkstra.html · https://cp-algorithms.com/graph/bellman_ford.html · https://leetcode.com/problems/network-delay-time/
- [ ] Minimum spanning tree: Prim / Kruskal (know the idea) ↳ https://cp-algorithms.com/graph/mst_prim.html · https://cp-algorithms.com/graph/mst_kruskal.html · https://leetcode.com/problems/min-cost-to-connect-all-points/

**Questions:** Number of Islands (200) · Clone Graph (133) · Max Area of Island (695) · Pacific Atlantic Water
Flow (417) · Surrounded Regions (130) · Rotting Oranges (994) · Course Schedule I/II (207, 210) · Graph Valid Tree
(261) · Number of Connected Components (323) · Redundant Connection (684) · Word Ladder (127) · Network Delay
Time (743) · Cheapest Flights Within K Stops (787) · Min Cost to Connect All Points (1584)

## 2.14 Intervals
- [ ] Sort by start, merge overlapping ↳ NeetCode "Merge Intervals" video · https://leetcode.com/problems/merge-intervals/ · https://www.techinterviewhandbook.org/algorithms/interval/
- [ ] Insert interval; non-overlapping (greedy by end) ↳ NeetCode "Non-overlapping Intervals" video · https://leetcode.com/problems/insert-interval/ · https://leetcode.com/problems/non-overlapping-intervals/
- [ ] Meeting rooms (min-heap of end times or sweep line) ↳ NeetCode "Meeting Rooms II" video (LC 253 is premium; free on neetcode.io) · https://leetcode.com/problems/car-pooling/ (same sweep line)

**Questions:** Insert Interval (57) · Merge Intervals (56) · Non-overlapping Intervals (435) · Meeting Rooms I/II
(252, 253)

## 2.15 Greedy
- [ ] When greedy works (exchange argument, intuition) ↳ Abdul Bari "Greedy Method - Introduction" video · https://leetcode.com/problems/jump-game/ · https://leetcode.com/problems/non-overlapping-intervals/ (exchange argument)
- [ ] Jump game; gas station; partition labels ↳ NeetCode "Gas Station" video · https://leetcode.com/problems/jump-game-ii/ · https://leetcode.com/problems/partition-labels/

**Questions:** Maximum Subarray (53) · Jump Game I/II (55, 45) · Gas Station (134) · Hand of Straights (846) ·
Partition Labels (763) · Valid Parenthesis String (678)

## 2.16 Dynamic programming
- [ ] Recognise DP: optimal substructure + overlapping subproblems ↳ freeCodeCamp "Dynamic Programming - Learn to Solve Algorithmic Problems & Coding Challenges" (Alvin Zablan) video · https://cp-algorithms.com/dynamic_programming/intro-to-dp.html · https://www.techinterviewhandbook.org/algorithms/dynamic-programming/
- [ ] Top-down (memo) vs bottom-up (table); space optimisation to O(1)/O(n) ↳ NeetCode "Climbing Stairs" video · https://leetcode.com/problems/climbing-stairs/ · https://leetcode.com/problems/house-robber/
- [ ] 1D: climbing stairs, house robber, decode ways, coin change, LIS, word break ↳ NeetCode "1-D Dynamic Programming" section (https://neetcode.io/roadmap) · https://leetcode.com/problems/coin-change/ · https://leetcode.com/problems/longest-increasing-subsequence/
- [ ] 2D: unique paths, LCS, edit distance, 0/1 knapsack, partition equal subset sum ↳ NeetCode "Longest Common Subsequence" video · https://leetcode.com/problems/edit-distance/ · https://cp-algorithms.com/dynamic_programming/knapsack.html
- [ ] Interval DP and state machine DP (stock with cooldown) — know the idea ↳ NeetCode "Best Time to Buy and Sell Stock with Cooldown" video · https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/ · https://leetcode.com/problems/burst-balloons/ (interval DP)

**Questions:** Climbing Stairs (70) · House Robber I/II (198, 213) · Longest Palindromic Substring (5) · Decode
Ways (91) · Coin Change (322) · Maximum Product Subarray (152) · Word Break (139) · LIS (300) · Partition Equal
Subset Sum (416) · Unique Paths (62) · LCS (1143) · Edit Distance (72) · Best Time with Cooldown (309) ·
Coin Change II (518) · Target Sum (494)

## 2.17 Bit manipulation and math
- [ ] AND/OR/XOR/shift; x & (x-1) clears lowest set bit; XOR to find the single number ↳ https://www.techinterviewhandbook.org/algorithms/binary/ · https://leetcode.com/problems/single-number/ · https://leetcode.com/problems/number-of-1-bits/
- [ ] Overflow in JS (2⁵³) and Python (unbounded ints) ↳ https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER · https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt · https://leetcode.com/problems/reverse-integer/
- [ ] GCD, modular arithmetic, fast power ↳ https://cp-algorithms.com/algebra/euclid-algorithm.html · https://cp-algorithms.com/algebra/binary-exp.html · https://leetcode.com/problems/powx-n/

**Questions:** Single Number (136) · Number of 1 Bits (191) · Counting Bits (338) · Reverse Bits (190) ·
Missing Number (268) · Pow(x, n) (50)

## 2.18 Interview technique
- [ ] Clarify inputs/constraints/edge cases before coding ↳ https://www.techinterviewhandbook.org/coding-interview-techniques/ · https://interviewing.io (watch recorded mock interviews)
- [ ] Say the brute force and its complexity first ↳ https://www.techinterviewhandbook.org/coding-interview-techniques/ · NeetCode "Two Sum" video (brute force → hash map)
- [ ] Talk while coding; name variables clearly ↳ https://www.techinterviewhandbook.org/coding-interview-techniques/ · https://www.pramp.com (practise thinking aloud with a peer)
- [ ] Test with your own example + edge cases before saying "done" ↳ https://www.techinterviewhandbook.org/coding-interview-techniques/ · https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/ (edge cases per topic)
- [ ] Code in the language you'll use at work (Python or TypeScript) — be fluent with its built-ins ↳ https://docs.python.org/3/library/collections.html · https://docs.python.org/3/library/bisect.html · https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Map

## 2.19 Sorting and selection (do this early, before 2.2)
- [ ] Merge sort (stable, O(n log n), O(n) space) — write it from memory ↳ https://visualgo.net/en/sorting · https://leetcode.com/problems/sort-an-array/ · DDIA ch3 "SSTables and LSM-trees" (pdf p96–99; mergesort-style merge)
- [ ] Quick sort (partition schemes, average vs worst case, randomised pivot) — write it from memory ↳ Abdul Bari "Quick Sort Algorithm" video · https://visualgo.net/en/sorting · https://leetcode.com/problems/sort-an-array/
- [ ] Heap sort; counting sort / bucket sort / radix sort (when O(n) is possible) ↳ https://visualgo.net/en/sorting · https://leetcode.com/problems/top-k-frequent-elements/ (bucket sort) · https://leetcode.com/problems/sort-colors/ (counting sort)
- [ ] Stability and why it matters (sorting by two keys) ↳ https://docs.python.org/3/howto/sorting.html ("Sort Stability and Complex Sorts") · https://en.wikipedia.org/wiki/Sorting_algorithm#Stability
- [ ] Quickselect for k-th element (average O(n)) ↳ NeetCode "Kth Largest Element in an Array" video · https://leetcode.com/problems/kth-largest-element-in-an-array/ · https://en.wikipedia.org/wiki/Quickselect
- [ ] Custom comparators in Python (`key=`, `functools.cmp_to_key`) and JS (`(a, b) => a - b`, the default string-sort trap) ↳ https://docs.python.org/3/howto/sorting.html · https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort · https://leetcode.com/problems/largest-number/
- [ ] Built-in sorts: Timsort (Python, JS V8) — stable, O(n log n) ↳ https://en.wikipedia.org/wiki/Timsort · https://v8.dev/blog/array-sort

**Questions:** Sort Colors (75) · Kth Largest Element via quickselect (215) · Largest Number (179) · Sort an Array
(912, write merge sort) · Why is `[10, 9, 1].sort()` wrong in JS?

## 2.20 Less common structures (P2 — know the idea, code only if time allows)
- [ ] Segment tree / Fenwick (binary indexed) tree: range sum with updates ↳ https://cp-algorithms.com/data_structures/segment_tree.html · https://cp-algorithms.com/data_structures/fenwick.html · https://leetcode.com/problems/range-sum-query-mutable/
- [ ] Ordered map / TreeMap (Python `sortedcontainers`, no built-in in JS) ↳ https://grantjenks.com/docs/sortedcontainers/ · DBI ch7 "Skiplist" (pdf p249–252) · https://leetcode.com/problems/my-calendar-i/
- [ ] String matching: KMP / rolling hash (Rabin-Karp) idea ↳ https://cp-algorithms.com/string/prefix-function.html · https://cp-algorithms.com/string/rabin-karp.html · https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/
- [ ] Reservoir sampling; random shuffle (Fisher–Yates) ↳ DMLS ch4 "Reservoir Sampling" (pdf p106–107) · https://leetcode.com/problems/linked-list-random-node/ · https://leetcode.com/problems/shuffle-an-array/
- [ ] Sieve of Eratosthenes; matrix exponentiation (rare) ↳ https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html · https://cp-algorithms.com/algebra/binary-exp.html (matrix power) · https://leetcode.com/problems/count-primes/

**Questions:** Range Sum Query – Mutable (307) · Implement strStr (28) · Shuffle an Array (384) · Random Pick with
Weight (528)
