# 4. DSA — data structures, algorithms and the systems they power

DSA rounds at Indian product companies and startups expect LeetCode mediums in about 25 minutes: clarify, say the
brute force, optimise, code cleanly, dry-run, and state time and space. For a 3-year backend + AI engineer they
also ask where these structures live in real systems (B-trees in Postgres, skip lists in Redis, HNSW in Qdrant).
Syllabus: DSA — NeetCode 150 + DSA ↔ Real Systems Mapping (`../../syllabus.html`).

## 4.1 Complexity analysis, recursion and the call stack
**Learn:** https://www.bigocheatsheet.com · https://neetcode.io/courses · https://wiki.python.org/moin/TimeComplexity · https://usaco.guide/bronze/time-comp · *Introduction to Algorithms* (CLRS) ch3–4
- [ ] `L1` What do Big-O, Big-Θ and Big-Ω describe? ↳ upper, tight and lower bounds on growth
- [ ] `L1` Best, average and worst case — is that the same thing as O, Θ and Ω? ↳ no: cases pick inputs; O/Θ/Ω bound functions
- [ ] `L1` Rank these: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ), O(n!).
- [ ] `L1` What is space complexity? Does the input itself count? ↳ auxiliary vs total space; say which you mean
- [ ] `L1` Why do we drop constants and lower-order terms? When do constants matter in practice?
- [ ] `L1` What is the complexity of a loop that halves `n` each step? Of a nested loop where the inner one runs `i` times?
- [ ] `L2` Why is appending to a dynamic array (Python `list`, JS array) O(1) amortised? ↳ geometric growth; total copying ≤ 2n
- [ ] `L2` What is amortised analysis? Aggregate vs accounting vs potential method, one line each.
- [ ] `L2` Amortised vs average case: what is the difference? ↳ amortised is a guarantee over any sequence; average assumes a distribution
- [ ] `L2` If a dynamic array grew by +10 slots instead of doubling, what would append cost? ↳ O(n) amortised: arithmetic series of copies
- [ ] `L2` Why is hash map lookup "O(1)", and when is it O(n)? ↳ average with good hash and bounded load; collisions, adversarial keys
- [ ] `L2` Given n ≤ 10⁵, which complexities fit a 1-second limit? n ≤ 20? n ≤ 10⁹? ↳ ~10⁸ simple ops/s: n log n; 2ⁿ; log n
- [ ] `L2` Cost of `x in list` vs `x in set` in Python? Of `arr.includes(x)` vs `set.has(x)` in JS?
- [ ] `L2` What does building a string with `+=` in a loop cost in Python and JS, and what do you do instead? ↳ immutable strings → O(n²) worst; join / array push
- [ ] `L2` Why can't a comparison sort beat O(n log n)? ↳ decision tree with n! leaves; log(n!) = Θ(n log n)
- [ ] `L2` How do you state complexity with two inputs (graph V and E, two strings m and n)?
- [ ] `L3` Why is building a heap bottom-up O(n), not O(n log n)? ↳ most nodes sit near leaves; sum of heights is O(n)
- [ ] `L3` What is pseudo-polynomial time? Why is the 0/1 knapsack DP not "polynomial"? ↳ polynomial in value W, exponential in its bit length
- [ ] `L3` What does Big-O hide that bites you in production? ↳ constants, cache misses, allocation, GC, I/O dominating CPU
- [ ] `L3` P, NP, NP-complete in one sentence each — and an NP-hard problem you would meet at work. ↳ scheduling, bin packing → heuristics, approximation

### Recursion and the call stack
- [ ] `L1` What happens on the call stack when a function calls itself? What is in a stack frame?
- [ ] `L1` What two parts does every recursive function need? What is Python's default recursion limit? ↳ base case + progress; ~1000, RecursionError
- [ ] `L2` What is the space complexity of recursive DFS on a balanced tree? On a skewed tree? ↳ O(h): O(log n) vs O(n)
- [ ] `L2` Draw the recursion tree for naive Fibonacci. What is its complexity, and what does memoisation change?
- [ ] `L2` State the Master theorem idea and solve T(n)=2T(n/2)+n, T(n)=T(n/2)+1, T(n)=2T(n/2)+1. ↳ n log n; log n; n
- [ ] `L2` What is tail recursion? Do CPython or V8 optimise it? ↳ no tail-call optimisation in either
- [ ] `L2` What does slicing `arr[1:]` cost inside a recursive function, and what do you pass instead? ↳ O(k) copy per call; pass indices
- [ ] `L2` How does `functools.lru_cache` / `@cache` turn exponential recursion into polynomial? What are its pitfalls? ↳ hashable args, unbounded memory, depth unchanged
- [ ] `L3` Your recursive solution crashes in Python at n = 10⁵. What are your options? ↳ explicit stack, bottom-up, raise limit + bigger thread stack
- [ ] `L3` Convert a recursive DFS to an iterative one with an explicit stack. Where do pre- and post-order work go?

## 4.2 How to approach a coding round
**Learn:** https://www.techinterviewhandbook.org/coding-interview-techniques/ · https://www.techinterviewhandbook.org/algorithms/study-cheatsheet/ · https://interviewing.io · https://docs.python.org/3/library/collections.html · https://docs.python.org/3/library/bisect.html
- [ ] `L1` What do you do in the first three minutes after hearing a problem? ↳ restate, clarify, small example, edge cases, constraints
- [ ] `L1` Which clarifying questions do you always ask? ↳ size, value ranges, negatives, duplicates, sorted, empty, in-place, output format
- [ ] `L1` Why say the brute force and its complexity out loud before optimising?
- [ ] `L1` Which edge cases do you test before saying "done"? ↳ empty, one element, duplicates, negatives, all equal, overflow, max size
- [ ] `L2` How do you go from brute force to optimal? Name the usual moves. ↳ hash/prefix precompute, sort, two pointers, heap, binary search, DP
- [ ] `L2` How do constraints hint at the intended complexity? ↳ n≤20 → 2ⁿ; 10³ → n²; 10⁵ → n log n
- [ ] `L2` You are stuck 15 minutes in. What do you say and do?
- [ ] `L2` How do you dry-run code on an example without running it, and what do you track?
- [ ] `L2` The interviewer asks "can you do better?" How do you decide if better is possible? ↳ lower bounds: must read input; sorting bound
- [ ] `L2` Python: which built-ins must you know cold? ↳ deque, Counter, defaultdict, heapq, bisect, itertools, functools.cache, sort keys
- [ ] `L2` TypeScript/JS: which built-ins do you rely on, and what is missing? ↳ Map, Set, array methods; no heap, deque, sorted map
- [ ] `L2` `array.shift()` in JS is O(n). How do you write a fast queue for BFS? ↳ head index pointer, or ring buffer
- [ ] `L2` How do you explain complexity at the end — what exactly do you say?
- [ ] `L3` Machine coding round (90 min: parking lot, Splitwise, snake game): how is it scored differently from DSA? ↳ runnable code, extensibility, clean classes, separation, tests
- [ ] `L3` You spot a bug after the interviewer has moved on. Do you raise it? How?
- [ ] `L3` How do you practise so NeetCode 150 patterns stick? ↳ timed 25 min, redo failures after 3 days, explain aloud

## 4.3 Arrays & Hashing
**Learn:** https://neetcode.io/roadmap (Arrays & Hashing) · https://www.techinterviewhandbook.org/algorithms/array/ · https://www.techinterviewhandbook.org/algorithms/string/ · https://cp-algorithms.com/string/prefix-function.html · https://cp-algorithms.com/string/rabin-karp.html
- [ ] `L1` Array vs linked list: access, insert and delete costs, and memory layout.
- [ ] `L1` When do you reach for a hash map in an array problem? ↳ seen-before, counts, complement lookup, grouping by key
- [ ] `L1` **Contains Duplicate** (LC 217) — three solutions and their costs. ↳ pairs n²; sort n log n; set O(n) space
- [ ] `L1` **Valid Anagram** (LC 242) — then: Unicode input? ↳ 26-count array vs hash map; sorting alternative
- [ ] `L1` **Two Sum** (LC 1) — then: input sorted? A stream of numbers? Duplicates? Return all pairs? ↳ two pointers if sorted; complement map; count map for duplicates
- [ ] `L1` Rotate or reverse an array in place: **Rotate Array** (LC 189), **Reverse String** (LC 344). ↳ triple-reverse trick
- [ ] `L1` **Move Zeroes** (LC 283) in place, keeping the order of non-zeros.
- [ ] `L2` What is a prefix sum, and which questions does it answer in O(1)?
- [ ] `L2` **Subarray Sum Equals K** (LC 560) — why does sliding window fail here? ↳ negatives; prefix sum + count map of seen sums
- [ ] `L2` What is a difference array? Solve **Corporate Flight Bookings** (LC 1109). ↳ +v at l, −v at r+1, one prefix pass
- [ ] `L2` **Group Anagrams** (LC 49) — which key, and what does it cost? ↳ sorted string O(k log k) vs 26-count tuple O(k)
- [ ] `L2` **Top K Frequent Elements** (LC 347) — heap vs bucket sort vs quickselect. ↳ O(n log k); O(n) buckets indexed by frequency
- [ ] `L2` **Encode and Decode Strings** (LC 271, premium; free on neetcode.io) — why does a plain delimiter break? ↳ length-prefix: `4#word`
- [ ] `L2` **Product of Array Except Self** (LC 238) without division — then with O(1) extra space. ↳ prefix pass, then suffix pass into output
- [ ] `L2` **Valid Sudoku** (LC 36) — how do you index the 3×3 boxes? ↳ (r//3, c//3); sets or bitmasks
- [ ] `L2` **Longest Consecutive Sequence** (LC 128) in O(n). ↳ set; only count up from numbers with no n−1
- [ ] `L2` **Design HashMap** (LC 706) from scratch — buckets, hash function, resizing.
- [ ] `L2` **Majority Element** (LC 169) in O(1) space. ↳ Boyer–Moore voting
- [ ] `L2` **Sort Colors** (LC 75) in one pass. ↳ Dutch national flag: low, mid, high pointers
- [ ] `L3` **Find the Index of the First Occurrence in a String** (LC 28) — naive vs KMP vs Rabin–Karp. ↳ prefix function O(n+m); rolling hash with collision check
- [ ] `L3` What is a rolling hash, and where else does it show up? ↳ rsync, content-defined chunking, dedup, plagiarism detection
- [ ] `L3` **First Missing Positive** (LC 41) in O(n) time and O(1) space. ↳ cyclic placement: value v to index v−1
- [ ] `L3` Two Sum over 10⁹ numbers that don't fit in memory. Now what? ↳ external sort + two pointers, or hash-partition into files

## 4.4 Two Pointers
**Learn:** https://neetcode.io/roadmap (Two Pointers) · https://www.techinterviewhandbook.org/algorithms/array/ · https://leetcode.com/problems/3sum/
- [ ] `L1` What is the two-pointer technique? Opposite ends vs same direction (fast/slow).
- [ ] `L1` When does two pointers need sorted input, and when doesn't it?
- [ ] `L1` **Valid Palindrome** (LC 125) — skip non-alphanumerics without building a new string.
- [ ] `L1` **Remove Duplicates from Sorted Array** (LC 26) in place — then allow at most two copies (LC 80).
- [ ] `L1` **Merge Sorted Array** (LC 88) in place — why fill from the back?
- [ ] `L2` **Two Sum II – Input Array Is Sorted** (LC 167) — prove the pointer moves never skip the answer. ↳ moving the smaller end discards only impossible pairs
- [ ] `L2` **3Sum** (LC 15) — how do you avoid duplicate triplets? ↳ sort; skip equal neighbours for i, l and r
- [ ] `L2` **4Sum** (LC 18) — how does the pattern generalise to k-sum? ↳ recurse down to 2-sum; O(n^(k−1))
- [ ] `L2` **Container With Most Water** (LC 11) — why move the shorter line? ↳ area capped by shorter side; moving taller can't help
- [ ] `L2` **Valid Palindrome II** (LC 680) — delete at most one character.
- [ ] `L2` **Squares of a Sorted Array** (LC 977) in O(n).
- [ ] `L2` Two pointers vs hash map for pair problems: time, space, and whether you need original indices.
- [ ] `L2` **Boats to Save People** (LC 881) — why pair the heaviest with the lightest?
- [ ] `L3` **Trapping Rain Water** (LC 42) — prefix-max arrays, then O(1) space; a monotonic-stack version also exists. ↳ water = min(maxLeft, maxRight) − height
- [ ] `L3` Merging two sorted streams that don't fit in memory is two pointers. Where does a database do this? ↳ merge join, LSM compaction, external sort

## 4.5 Sliding Window
**Learn:** https://neetcode.io/roadmap (Sliding Window) · https://leetcode.com/problems/minimum-window-substring/ · https://leetcode.com/problems/fruit-into-baskets/
- [ ] `L1` What is a sliding window? Fixed-size vs variable-size.
- [ ] `L1` What makes a problem a sliding-window problem? ↳ contiguous range; validity changes monotonically as window grows
- [ ] `L1` **Best Time to Buy and Sell Stock** (LC 121) — then unlimited trades (LC 122)? At most k trades? A fee? ↳ track min so far; sum positive diffs; DP for k
- [ ] `L1` **Maximum Average Subarray I** (LC 643) — fixed window in O(n).
- [ ] `L2` Write the variable-window template: expand right, shrink left while invalid, record the answer.
- [ ] `L2` Why is a variable window O(n) even with a nested `while`? ↳ each index enters and leaves once
- [ ] `L2` **Longest Substring Without Repeating Characters** (LC 3) — set version vs last-index map. ↳ left = max(left, last[c] + 1)
- [ ] `L2` **Longest Repeating Character Replacement** (LC 424) — why never decrease `maxFreq` when shrinking? ↳ the answer only grows when maxFreq grows
- [ ] `L2` **Permutation in String** (LC 567) — fixed window of counts; then O(n) with a "matches" counter.
- [ ] `L2` **Fruit Into Baskets** (LC 904) — longest window with at most K distinct values.
- [ ] `L2` **Minimum Size Subarray Sum** (LC 209) — then numbers can be negative? ↳ window breaks; prefix sums + monotonic deque (LC 862)
- [ ] `L2` "Exactly K" windows: **Subarrays with K Different Integers** (LC 992). ↳ atMost(K) − atMost(K−1)
- [ ] `L2` When does sliding window fail, and what do you use instead? ↳ negatives, non-monotonic validity, non-contiguous → prefix sums, DP
- [ ] `L3` **Minimum Window Substring** (LC 76) — `need`/`have` counters; why O(m + n)?
- [ ] `L3` **Sliding Window Maximum** (LC 239) — heap O(n log k) vs monotonic deque O(n). ↳ deque of indices, decreasing values; pop expired front
- [ ] `L3` Sliding windows in real systems — TCP window, rate-limiter windows, moving averages. How does each map to this pattern?

## 4.6 Stack and queue (monotonic stack, deque)
**Learn:** https://neetcode.io/roadmap (Stack) · https://www.techinterviewhandbook.org/algorithms/stack/ · https://cp-algorithms.com/data_structures/stack_queue_modification.html · https://docs.python.org/3/library/collections.html#collections.deque
- [ ] `L1` Stack vs queue vs deque: operations and costs. How do you get each in Python and JS?
- [ ] `L1` Why are `list.pop(0)` in Python and `shift()` in JS traps for queues? ↳ O(n) shifting; use deque or a head index
- [ ] `L1` **Valid Parentheses** (LC 20) — then with only one bracket type in O(1) space.
- [ ] `L1` **Min Stack** (LC 155) — O(1) `getMin`. ↳ second stack of mins, or (value, min) pairs
- [ ] `L1` **Implement Queue using Stacks** (LC 232) — why is it amortised O(1)?
- [ ] `L2` **Evaluate Reverse Polish Notation** (LC 150) — integer division toward zero in Python vs JS. ↳ int(a / b) in Python; Math.trunc in JS
- [ ] `L2` **Generate Parentheses** (LC 22) — what invariant keeps every string valid? ↳ open < n; close < open
- [ ] `L2` What is a monotonic stack, and what question shape does it answer? ↳ next/previous greater or smaller element in O(n)
- [ ] `L2` **Daily Temperatures** (LC 739) — brute force, then monotonic stack.
- [ ] `L2` **Next Greater Element II** (LC 503) — the circular version. ↳ loop 2n with index mod n
- [ ] `L2` **Car Fleet** (LC 853) — sort by position, then a stack of arrival times.
- [ ] `L2` **Online Stock Span** (LC 901) and **Asteroid Collision** (LC 735).
- [ ] `L2` **Decode String** (LC 394) — `3[a2[c]]`.
- [ ] `L2` **Basic Calculator II** (LC 227) — then with parentheses (LC 224). ↳ stack of terms; recursion or sign stack for parens
- [ ] `L3` **Largest Rectangle in Histogram** (LC 84) — why is each bar pushed and popped once? ↳ width spans previous smaller to next smaller
- [ ] `L3` **Maximal Rectangle** (LC 85) — reduce to a histogram per row.
- [ ] `L3` **Sum of Subarray Minimums** (LC 907) — count each element's contribution. ↳ strict on one side, non-strict on the other for ties
- [ ] `L3` **Remove K Digits** (LC 402) — greedy with a monotonic stack.

## 4.7 Binary Search
**Learn:** https://neetcode.io/roadmap (Binary Search) · DBI ch4 "Binary Search" (pdf p123–125) · https://docs.python.org/3/library/bisect.html · https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/
- [ ] `L1` What does binary search need from the input, and what is its complexity?
- [ ] `L1` **Binary Search** (LC 704) — `lo <= hi` vs `lo < hi`: which update goes with which?
- [ ] `L1` Why write `mid = lo + (hi - lo) // 2`? Does it matter in Python? In JS? In Java? ↳ overflow only with fixed-width ints
- [ ] `L1` What do `bisect_left` and `bisect_right` return? **Search Insert Position** (LC 35).
- [ ] `L2` **Find First and Last Position of Element in Sorted Array** (LC 34) — lower bound and upper bound.
- [ ] `L2` What is binary search on the answer space, and how do you spot it? ↳ monotonic yes/no feasibility over a numeric range
- [ ] `L2` **Search a 2D Matrix** (LC 74) as a 1-D array — then **Search a 2D Matrix II** (LC 240). ↳ staircase from top-right corner
- [ ] `L2` **Koko Eating Bananas** (LC 875) — bounds, feasibility check, rounding. ↳ lo = 1, hi = max(piles); ceiling division
- [ ] `L2` **Capacity To Ship Packages Within D Days** (LC 1011).
- [ ] `L2` **Find Minimum in Rotated Sorted Array** (LC 153) — then with duplicates (LC 154). ↳ compare mid to hi; duplicates → hi−1, worst O(n)
- [ ] `L2` **Search in Rotated Sorted Array** (LC 33) — which half is sorted?
- [ ] `L2` **Time Based Key-Value Store** (LC 981) — why binary search works; what if timestamps arrive out of order? ↳ appends already sorted; otherwise insort or sorted container
- [ ] `L2` **Find Peak Element** (LC 162) — why does binary search work on an unsorted array?
- [ ] `L2` **Sqrt(x)** (LC 69) without floats — then binary search over real numbers: when do you stop?
- [ ] `L3` **Median of Two Sorted Arrays** (LC 4) in O(log min(m, n)). ↳ partition smaller array; maxLeft ≤ minRight on both sides
- [ ] `L3` **Split Array Largest Sum** (LC 410) — binary search on the answer vs DP.
- [ ] `L3` How does a B-tree page lookup use binary search over its cells? ↳ slotted page: binary search on sorted cell-offset array
- [ ] `L3` `git bisect` is binary search. Where else have you binary-searched in production (bad deploy, log time range)?

## 4.8 Linked Lists
**Learn:** https://neetcode.io/roadmap (Linked List) · https://visualgo.net/en/list · DDIA ch3 "SSTables and LSM-Trees" (pdf p96–99; merging sorted segments)
- [ ] `L1` Singly vs doubly linked list: costs, and when you would use each.
- [ ] `L1` What is the dummy (sentinel) head trick, and which edge cases does it remove?
- [ ] `L1` **Reverse Linked List** (LC 206) — iterative and recursive. Space of each? ↳ O(1) vs O(n) call stack
- [ ] `L1` **Merge Two Sorted Lists** (LC 21).
- [ ] `L1` **Linked List Cycle** (LC 141) — hash set vs Floyd's tortoise and hare.
- [ ] `L1` **Middle of the Linked List** (LC 876) — which middle for even length?
- [ ] `L2` **Linked List Cycle II** (LC 142) — why does restarting one pointer at head find the cycle start? ↳ head→start distance ≡ meet→start distance mod cycle length
- [ ] `L2` **Reorder List** (LC 143) — find middle, reverse second half, merge.
- [ ] `L2` **Remove Nth Node From End of List** (LC 19) in one pass.
- [ ] `L2` **Copy List with Random Pointer** (LC 138) — hash map vs interleaving in O(1) space.
- [ ] `L2` **Add Two Numbers** (LC 2) — then digits stored most-significant first (LC 445). ↳ stacks or reverse; carry at the end
- [ ] `L2` **Find the Duplicate Number** (LC 287) — why is this a cycle problem? ↳ index → value as next pointer; Floyd; O(1) space
- [ ] `L2` **Palindrome Linked List** (LC 234) in O(1) space — and restore the list afterwards.
- [ ] `L2` **Intersection of Two Linked Lists** (LC 160) — the switch-heads trick.
- [ ] `L2` **Sort List** (LC 148) — why merge sort and not quicksort for linked lists? ↳ no random access; merge needs O(1) extra on lists
- [ ] `L3` **Merge K Sorted Lists** (LC 23) — heap vs divide-and-conquer pairing. ↳ both O(N log k); heap suits streams
- [ ] `L3` **Reverse Nodes in k-Group** (LC 25) — what happens to a last group shorter than k?
- [ ] `L3` **Linked List Random Node** (LC 382) when the length is unknown. ↳ reservoir sampling: keep i-th with probability 1/i
- [ ] `L3` Why are linked lists slow on modern CPUs even though iteration is O(n), and what do real systems use instead? ↳ pointer chasing, cache misses; arrays, unrolled lists, arenas

## 4.9 Trees
**Learn:** https://neetcode.io/roadmap (Trees) · https://visualgo.net/en/bst · DBI ch2 "Binary Search Trees" (pdf p57–62) · DBI ch2 "Tree Balancing" (pdf p59–61)
- [ ] `L1` Define binary tree, BST, complete, full, perfect and balanced tree. Height vs depth.
- [ ] `L1` Preorder, inorder, postorder, level order — what is each one good for? ↳ copy/serialize; sorted BST output; children-first work; levels
- [ ] `L1` DFS vs BFS on a tree: space for a wide tree vs a deep tree. ↳ DFS O(height); BFS O(max width)
- [ ] `L1` **Invert Binary Tree** (LC 226).
- [ ] `L1` **Maximum Depth of Binary Tree** (LC 104) — recursive, BFS, and iterative DFS.
- [ ] `L1` **Same Tree** (LC 100) and **Symmetric Tree** (LC 101).
- [ ] `L1` **Subtree of Another Tree** (LC 572) — O(m·n), then O(m + n) with serialization + KMP or tree hashing.
- [ ] `L1` **Lowest Common Ancestor of a Binary Search Tree** (LC 235) — use the BST property.
- [ ] `L2` **Binary Tree Inorder Traversal** (LC 94) iteratively with a stack — then in O(1) space? ↳ Morris traversal threads predecessors' right pointers
- [ ] `L2` **Diameter of Binary Tree** (LC 543) — why does the answer live outside the return value? ↳ return height; update best with left + right
- [ ] `L2` **Balanced Binary Tree** (LC 110) in O(n). ↳ return height, or −1 for unbalanced
- [ ] `L2` **Binary Tree Level Order Traversal** (LC 102) — then zigzag (LC 103).
- [ ] `L2` **Binary Tree Right Side View** (LC 199) — BFS last-of-level vs DFS right-first.
- [ ] `L2` **Count Good Nodes in Binary Tree** (LC 1448) — pass the max down.
- [ ] `L2` **Validate Binary Search Tree** (LC 98) — why is checking parent vs child wrong? ↳ pass (low, high) bounds, or strictly increasing inorder
- [ ] `L2` **Kth Smallest Element in a BST** (LC 230) — then the tree changes often and k-th is queried often. ↳ augment nodes with subtree sizes
- [ ] `L2` **Construct Binary Tree from Preorder and Inorder Traversal** (LC 105) — why a hash map of inorder positions?
- [ ] `L2` **Lowest Common Ancestor of a Binary Tree** (LC 236) — then with parent pointers; then many queries. ↳ parent pointers → list intersection; binary lifting for many queries
- [ ] `L2` **Path Sum** (LC 112) → **Path Sum III** (LC 437): how does a prefix sum work on a tree? ↳ prefix counts along root path; undo on backtrack
- [ ] `L2` BST insert, search and delete — the three delete cases. ↳ leaf; one child; two children → inorder successor
- [ ] `L2` Why can a BST degrade to O(n)? Name self-balancing trees and where they are used. ↳ AVL, red-black: Java TreeMap, C++ std::map, Linux CFS
- [ ] `L3` **Binary Tree Maximum Path Sum** (LC 124) — what do you return vs what do you record? ↳ return best single branch ≥ 0; record left + node + right
- [ ] `L3` **Serialize and Deserialize Binary Tree** (LC 297) — then for a BST in less space (LC 449). ↳ BST: preorder alone, bounds rebuild it
- [ ] `L3` **Vertical Order Traversal of a Binary Tree** (LC 987) — how are ties ordered?
- [ ] `L3` Why do databases use B-trees instead of binary search trees? ↳ high fanout → few page reads; height 3–4
- [ ] `L3` How did you store a tree (comments, org chart, categories) in Postgres at work? ↳ adjacency list + recursive CTE, materialized path, closure table, ltree

## 4.10 Tries
**Learn:** https://neetcode.io/roadmap (Tries) · DDIA ch3 "Other indexing structures" (pdf p107; trie-like automaton in Lucene) · https://leetcode.com/problems/implement-trie-prefix-tree/
- [ ] `L1` What is a trie, and what does each node hold? ↳ children map or array, end-of-word flag, optional count/payload
- [ ] `L1` Trie vs a hash set of words: what can a trie do that a set can't? ↳ prefix queries, sorted iteration, longest-prefix match
- [ ] `L1` **Implement Trie (Prefix Tree)** (LC 208) — cost of insert, search and `startsWith`. ↳ O(L) per operation
- [ ] `L2` Children as a 26-slot array vs a hash map: memory and speed trade-offs.
- [ ] `L2` **Design Add and Search Words Data Structure** (LC 211) — what does `.` do to the complexity?
- [ ] `L2` **Word Search II** (LC 212) — why a trie of the words instead of searching each word? Which pruning matters? ↳ one DFS per cell; prune found words and dead leaves
- [ ] `L2` **Replace Words** (LC 648) — shortest root prefix per word.
- [ ] `L2` **Search Suggestions System** (LC 1268) — trie vs sort + binary search.
- [ ] `L2` **Maximum XOR of Two Numbers in an Array** (LC 421) with a bitwise trie. ↳ insert bits MSB-first; greedily take the opposite bit
- [ ] `L3` A trie of 10M words uses too much memory. How do you shrink it? ↳ radix/Patricia compression, DAWG/FST, array-packed nodes

### Tries for autocomplete and routing
- [ ] `L2` Design search-box autocomplete: top 5 suggestions for a prefix in under 50 ms. ↳ trie with cached top-k per node, or sorted list + bisect
- [ ] `L2` How do you keep per-node top-k fresh when query counts change hourly? ↳ rebuild offline in batches, swap atomically
- [ ] `L2` What is a radix tree, and where do HTTP routers use one? ↳ compressed trie; Fastify's find-my-way, Go httprouter
- [ ] `L3` How would you shard an autocomplete trie across machines? ↳ by prefix range; replicate hot prefixes; cache at edge
- [ ] `L3` Longest-prefix match for IP routing: why a trie?
- [ ] `L3` How does Lucene / Elasticsearch store its term dictionary? ↳ FST: minimised trie-like automaton
- [ ] `L3` Fuzzy autocomplete that tolerates typos: what would you add? ↳ edit-distance search over trie, BK-tree, n-gram index

## 4.11 Heaps / Priority Queues
**Learn:** https://neetcode.io/roadmap (Heap / Priority Queue) · https://docs.python.org/3/library/heapq.html · https://visualgo.net/en/heap · DBI ch7 "Merge-Iteration" (pdf p232–236; min-heap k-way merge)
- [ ] `L1` What is a binary heap, and how is it stored in an array? ↳ parent (i−1)//2; children 2i+1, 2i+2
- [ ] `L1` Costs of push, pop, peek and heapify. ↳ log n, log n, 1, n
- [ ] `L1` Python `heapq` is min-heap only. How do you get a max-heap? How do you break ties in tuples? ↳ negate; (priority, counter, item)
- [ ] `L1` JavaScript has no heap. What do you do in an interview? ↳ write a ~30-line binary heap
- [ ] `L1` Heap vs sorted array vs balanced BST as a priority queue.
- [ ] `L1` **Last Stone Weight** (LC 1046).
- [ ] `L1` **Kth Largest Element in a Stream** (LC 703) — why a min-heap of size k?
- [ ] `L2` Write sift-up and sift-down from memory.
- [ ] `L2` **K Closest Points to Origin** (LC 973) — heap O(n log k) vs quickselect O(n) average.
- [ ] `L2` **Kth Largest Element in an Array** (LC 215) — sort, heap, quickselect: which do you code first? ↳ quickselect average O(n), worst O(n²); random pivot
- [ ] `L2` **Task Scheduler** (LC 621) — heap + cooldown queue simulation vs the counting formula. ↳ (maxFreq−1)·(n+1) + countOfMax, at least len(tasks)
- [ ] `L2` **Design Twitter** (LC 355) — build the news feed by merging users' tweet lists. ↳ k-way heap merge; fan-out on write vs read
- [ ] `L2` **Reorganize String** (LC 767) — greedy with a max-heap.
- [ ] `L2` How do you change the priority of an item already in the heap? ↳ lazy deletion with a removed set, or indexed heap
- [ ] `L2` **Single-Threaded CPU** (LC 1834) — simulate a scheduler with two orderings.
- [ ] `L3` **Find Median from Data Stream** (LC 295) — two heaps; then 99% of values are in [0, 100]? ↳ counting buckets plus heaps for outliers
- [ ] `L3` **Smallest Range Covering Elements from K Lists** (LC 632).
- [ ] `L3` Top-K heavy hitters over an unbounded stream that doesn't fit in memory. ↳ Count-Min Sketch + heap; Space-Saving / Misra–Gries
- [ ] `L3` How do Python's `asyncio` and Node's libuv find the next timer to fire? ↳ both keep a min-heap of timers
- [ ] `L3` Low-priority jobs never run in your priority queue. How do you fix starvation? ↳ aging: raise priority with waiting time

## 4.12 Backtracking
**Learn:** https://neetcode.io/roadmap (Backtracking) · https://www.techinterviewhandbook.org/algorithms/recursion/ · https://leetcode.com/problems/n-queens/
- [ ] `L1` What is backtracking? Write the choose → explore → un-choose template.
- [ ] `L1` Backtracking vs brute force vs DP: what is the difference?
- [ ] `L1` **Subsets** (LC 78) — recursion vs iteration vs bitmask. How many subsets? ↳ 2ⁿ; O(n·2ⁿ) to output
- [ ] `L1` **Permutations** (LC 46) — swap in place vs `used[]`. How many? ↳ n!
- [ ] `L1` **Letter Combinations of a Phone Number** (LC 17).
- [ ] `L2` **Combination Sum** (LC 39) — reuse numbers without duplicate combinations. ↳ recurse with same index; never revisit earlier indices
- [ ] `L2` **Subsets II** (LC 90) — skip duplicates after sorting. ↳ skip nums[i] == nums[i−1] when i > start
- [ ] `L2` **Combination Sum II** (LC 40) — each number once, no duplicate combinations.
- [ ] `L2` **Permutations II** (LC 47) with duplicate values.
- [ ] `L2` **Word Search** (LC 79) — mark visited in place; what is the complexity? ↳ O(m·n·3^L) roughly
- [ ] `L2` **Palindrome Partitioning** (LC 131) — precompute a palindrome table to speed it up.
- [ ] `L2` Why must you copy the path when you record a result (`path[:]`, `[...path]`)? ↳ shared mutable list changes later
- [ ] `L2` What is pruning? Give two examples that change the runtime a lot.
- [ ] `L2` How do you estimate backtracking complexity for the interviewer? ↳ branching factor^depth × work per leaf
- [ ] `L3` **N-Queens** (LC 51) — O(1) conflict checks. ↳ sets for columns, r−c and r+c diagonals
- [ ] `L3` **Sudoku Solver** (LC 37) — which cell do you try first? ↳ most constrained cell; bitmasks per row/col/box
- [ ] `L3` **Word Break II** (LC 140) — backtracking plus memo.
- [ ] `L3` **Partition to K Equal Sum Subsets** (LC 698) — pruning and bitmask memo.

## 4.13 Graphs — traversal, grids, topological sort, cycles
**Learn:** https://neetcode.io/roadmap (Graphs) · https://cp-algorithms.com/graph/breadth-first-search.html · https://cp-algorithms.com/graph/topological-sort.html · https://cp-algorithms.com/graph/finding-cycle.html · https://visualgo.net/en/dfsbfs · DDIA ch2 "Graph-like Data Models" (pdf p70–84)
- [ ] `L1` Adjacency list vs adjacency matrix vs edge list: memory and when to use each. ↳ list O(V+E) for sparse; matrix O(V²), O(1) edge check
- [ ] `L1` BFS vs DFS: which gives shortest paths in an unweighted graph, and why?
- [ ] `L1` Complexity of BFS/DFS on a graph and on an m×n grid. ↳ O(V + E); O(m·n)
- [ ] `L1` Why do you need a visited set in a graph but not in a tree? Mark on push or on pop? ↳ BFS: mark on push to avoid duplicate enqueues
- [ ] `L1` **Flood Fill** (LC 733).
- [ ] `L1` **Number of Islands** (LC 200) — DFS, BFS and union-find; then the grid is too big for recursion. ↳ iterative BFS; mutate grid or keep visited
- [ ] `L2` **Max Area of Island** (LC 695).
- [ ] `L2` **Clone Graph** (LC 133) — the old → new node map.
- [ ] `L2` **Pacific Atlantic Water Flow** (LC 417) — why search from the oceans inward? ↳ reverse flow: two multi-source searches, intersect
- [ ] `L2` **Surrounded Regions** (LC 130) — mark border-connected cells first.
- [ ] `L2` **Rotting Oranges** (LC 994) — multi-source BFS, counting minutes by level.
- [ ] `L2` **Walls and Gates** (LC 286, premium; free on neetcode.io) — multi-source BFS from every gate.
- [ ] `L2` **01 Matrix** (LC 542) — why multi-source BFS beats BFS from each cell.
- [ ] `L2` What is topological sort? Kahn's algorithm (indegree BFS) vs DFS post-order.
- [ ] `L2` **Course Schedule** (LC 207) and **Course Schedule II** (LC 210) — detect a cycle and return an order. ↳ Kahn: processed count < n means a cycle
- [ ] `L2` Cycle detection in a directed graph with three colours. Why isn't a visited set enough? ↳ grey = on current path; black = finished
- [ ] `L2` Cycle detection in an undirected graph: parent check vs union-find.
- [ ] `L2` **Graph Valid Tree** (LC 261, premium; free on neetcode.io). ↳ exactly n−1 edges and connected
- [ ] `L2` **Number of Connected Components in an Undirected Graph** (LC 323, premium; free on neetcode.io).
- [ ] `L2` **Word Ladder** (LC 127) — how do you find neighbours fast? Then bidirectional BFS. ↳ wildcard map `h*t`; search from both ends
- [ ] `L2` What is a bipartite graph? **Is Graph Bipartite?** (LC 785). ↳ two-colour BFS; odd cycle means not bipartite
- [ ] `L3` **Shortest Path to Get All Keys** (LC 864) — BFS over (cell, key bitmask) states.
- [ ] `L3` **Critical Connections in a Network** (LC 1192) — Tarjan's bridges with low-link values.
- [ ] `L3` Strongly connected components: Kosaraju vs Tarjan, and a real use.
- [ ] `L3` npm/pip dependency resolution, Makefiles, Airflow DAGs, Terraform: which algorithm runs underneath? ↳ topological sort + cycle detection
- [ ] `L3` How would you detect a deadlock among DB transactions? ↳ cycle in the wait-for graph
- [ ] `L3` How do you BFS a graph with 10 billion edges that doesn't fit on one machine? ↳ partitioned frontier per superstep (Pregel / BSP)

## 4.14 Advanced graphs — shortest paths, Union-Find, MST
**Learn:** https://neetcode.io/roadmap (Advanced Graphs) · https://cp-algorithms.com/graph/dijkstra.html · https://cp-algorithms.com/graph/bellman_ford.html · https://cp-algorithms.com/data_structures/disjoint_set_union.html · https://cp-algorithms.com/graph/mst_kruskal.html · https://cp-algorithms.com/graph/mst_prim.html
- [ ] `L1` Which shortest-path algorithm for: unweighted, non-negative weights, negative weights, all pairs, 0/1 weights? ↳ BFS; Dijkstra; Bellman–Ford; Floyd–Warshall; 0-1 BFS
- [ ] `L1` What is Union-Find (disjoint set union)? What do `find` and `union` do?
- [ ] `L1` What is a minimum spanning tree? Name two algorithms that build one.
- [ ] `L2` How does Dijkstra work with a heap? Why does it fail with negative edges? ↳ a settled node must never improve; negatives break that
- [ ] `L2` Dijkstra's complexity with a binary heap, and why stale heap entries are fine. ↳ O((V + E) log V); skip if popped dist > best
- [ ] `L2` **Network Delay Time** (LC 743).
- [ ] `L2` **Swim in Rising Water** (LC 778) — min-heap on max elevation vs binary search + BFS.
- [ ] `L2` **Path With Minimum Effort** (LC 1631).
- [ ] `L2` **Cheapest Flights Within K Stops** (LC 787) — why plain Dijkstra fails; Bellman–Ford with k+1 rounds. ↳ copy distances each round to cap edge count
- [ ] `L2` How does Bellman–Ford detect a negative cycle? Where do negative cycles matter? ↳ V-th round still relaxes; currency arbitrage
- [ ] `L2` Union-Find with path compression and union by rank: what does each give? ↳ near-constant α(n) amortised
- [ ] `L2` **Redundant Connection** (LC 684) — the first edge joining already-connected nodes.
- [ ] `L2` **Accounts Merge** (LC 721) — union-find over emails.
- [ ] `L2` **Min Cost to Connect All Points** (LC 1584) — Prim vs Kruskal on a dense graph. ↳ complete graph: O(V²) Prim without a heap
- [ ] `L2` **Reconstruct Itinerary** (LC 332) — Hierholzer's Eulerian path. ↳ lexical order; post-order append, then reverse
- [ ] `L2` **Alien Dictionary** (LC 269, premium; free on neetcode.io) — edges from adjacent words, then topo sort. ↳ trap: "abc" before "ab" is invalid
- [ ] `L3` Floyd–Warshall: complexity, and when it is fine. ↳ O(V³); fine up to a few hundred nodes
- [ ] `L3` A* search: what is a heuristic, and when is A* optimal? ↳ admissible: never overestimates; consistent
- [ ] `L3` How do map routers answer shortest-path queries in milliseconds? ↳ contraction hierarchies, precomputation, bidirectional A*
- [ ] `L3` Where would graph algorithms help in an LLM agent system (tool dependency DAG, workflow orchestration)?

## 4.15 1-D Dynamic Programming
**Learn:** https://neetcode.io/roadmap (1-D Dynamic Programming) · https://cp-algorithms.com/dynamic_programming/intro-to-dp.html · https://www.techinterviewhandbook.org/algorithms/dynamic-programming/ · freeCodeCamp "Dynamic Programming" (Alvin Zablan) video
- [ ] `L1` Which two properties make a problem a DP problem? ↳ optimal substructure, overlapping subproblems
- [ ] `L1` Top-down memoisation vs bottom-up tabulation: trade-offs.
- [ ] `L1` DP vs greedy vs divide and conquer.
- [ ] `L1` **Climbing Stairs** (LC 70) — then steps {1, 3, 5}; then n = 10¹⁸. ↳ general recurrence; matrix exponentiation for huge n
- [ ] `L1` **Min Cost Climbing Stairs** (LC 746).
- [ ] `L2` How do you define the state and transition? Walk through your recipe. ↳ state, recurrence, base cases, iteration order, answer cell
- [ ] `L2` **House Robber** (LC 198) and **House Robber II** (LC 213) — circular street. ↳ run twice: skip first, skip last
- [ ] `L2` **Longest Palindromic Substring** (LC 5) — DP table vs expand around centre. ↳ expand: O(n²) time, O(1) space; Manacher O(n)
- [ ] `L2` **Palindromic Substrings** (LC 647).
- [ ] `L2` **Decode Ways** (LC 91) — the zero traps. ↳ "0" alone invalid; "10", "20" valid; "30" invalid
- [ ] `L2` **Coin Change** (LC 322) — why greedy fails; then return the coins used. ↳ coins {1, 3, 4}, amount 6; parent pointers
- [ ] `L2` **Maximum Product Subarray** (LC 152) — why track the min as well as the max?
- [ ] `L2` **Word Break** (LC 139) — DP over prefixes; then with a trie for a long dictionary.
- [ ] `L2` **Longest Increasing Subsequence** (LC 300) — O(n²) DP, then O(n log n). ↳ tails array + bisect_left (patience sorting)
- [ ] `L2` **Partition Equal Subset Sum** (LC 416) — 1-D boolean knapsack; why iterate sums backwards? ↳ each item used at most once
- [ ] `L2` **Combination Sum IV** (LC 377) vs **Coin Change II** — does order matter, and how does the loop change?
- [ ] `L2` How do you reduce O(n) DP space to O(1)?
- [ ] `L3` **Russian Doll Envelopes** (LC 354) — the sort trick, then LIS. ↳ width ascending, height descending; LIS on heights
- [ ] `L3` **Best Time to Buy and Sell Stock IV** (LC 188) — state machine DP with k transactions.
- [ ] `L3` Where does DP show up in real systems? ↳ diff (LCS), spell check, Viterbi, query-planner join ordering

## 4.16 2-D Dynamic Programming
**Learn:** https://neetcode.io/roadmap (2-D Dynamic Programming) · https://cp-algorithms.com/dynamic_programming/knapsack.html · *Introduction to Algorithms* (CLRS) ch15 "Dynamic Programming"
- [ ] `L1` What makes a DP "2-D"? Give three typical state shapes. ↳ (row, col); (i, j) over two strings; (item, capacity)
- [ ] `L1` **Unique Paths** (LC 62) — DP, then combinatorics; then with obstacles (LC 63). ↳ C(m+n−2, m−1)
- [ ] `L1` **Minimum Path Sum** (LC 64).
- [ ] `L2` **Longest Common Subsequence** (LC 1143) — what a cell means, then rebuild the subsequence.
- [ ] `L2` Longest common subsequence vs longest common substring: how does the recurrence change? ↳ substring resets to 0 on mismatch
- [ ] `L2` **Edit Distance** (LC 72) — the three operations in the recurrence; then O(min(m, n)) space.
- [ ] `L2` 0/1 knapsack vs unbounded knapsack: what changes in loop order? ↳ 0/1 capacity backwards; unbounded forwards
- [ ] `L2` **Coin Change II** (LC 518) — why put coins in the outer loop to count combinations?
- [ ] `L2` **Target Sum** (LC 494) — reduce to subset sum. ↳ P = (sum + target)/2, where P is the positive-set sum
- [ ] `L2` **Best Time to Buy and Sell Stock with Cooldown** (LC 309) — states held, sold, rest.
- [ ] `L2` **Interleaving String** (LC 97).
- [ ] `L2` **Longest Increasing Path in a Matrix** (LC 329) — DFS + memo; why no visited set? ↳ strictly increasing → no cycles: a DAG
- [ ] `L2` **Maximal Square** (LC 221).
- [ ] `L2` **Longest Palindromic Subsequence** (LC 516) — LCS with the reverse string.
- [ ] `L3` **Distinct Subsequences** (LC 115).
- [ ] `L3` **Burst Balloons** (LC 312) — interval DP: think of the last balloon burst. ↳ dp[l][r] = max over k burst last
- [ ] `L3` **Regular Expression Matching** (LC 10) — handling `*` as zero or more. ↳ `*` skips the pair or consumes one matching char
- [ ] `L3` **Wildcard Matching** (LC 44) — how does it differ from regex matching?
- [ ] `L3` How does `git diff` use LCS, and why is Myers' algorithm faster than the full table? ↳ O((m + n)·D), D = edit size
- [ ] `L3` Where would edit distance help in your work? ↳ fuzzy name matching, typo-tolerant search, LLM output evaluation

## 4.17 Greedy
**Learn:** https://neetcode.io/roadmap (Greedy) · Abdul Bari "Greedy Method - Introduction" video · https://leetcode.com/problems/jump-game-ii/
- [ ] `L1` What is a greedy algorithm, and why does a greedy solution need a proof?
- [ ] `L1` **Maximum Subarray** (LC 53) — Kadane; then return indices; then circular (LC 918). ↳ circular: max(kadane, total − min subarray); all-negative case
- [ ] `L1` **Jump Game** (LC 55) — track the furthest reachable index.
- [ ] `L2` How do you prove a greedy choice is safe? Explain the exchange argument. ↳ swap optimal's choice for greedy's without making it worse
- [ ] `L2` Give a problem where greedy looks right but fails. ↳ coin change {1, 3, 4}; 0/1 knapsack
- [ ] `L2` **Jump Game II** (LC 45) — BFS by levels in O(1) space.
- [ ] `L2` **Gas Station** (LC 134) — why reset the start after a negative tank? ↳ total ≥ 0 guarantees a start; failed segment can't hold it
- [ ] `L2` **Hand of Straights** (LC 846) — always start groups from the smallest card.
- [ ] `L2` **Merge Triplets to Form Target Triplet** (LC 1899).
- [ ] `L2` **Partition Labels** (LC 763) — last-occurrence map.
- [ ] `L2` **Valid Parenthesis String** (LC 678) — track a range of possible open counts. ↳ [minOpen, maxOpen] beats DP and two stacks
- [ ] `L2` **Candy** (LC 135) — two passes.
- [ ] `L2` Interval scheduling: why sort by end time, not start time?
- [ ] `L3` Huffman coding — greedy with a heap. Where is it used? ↳ DEFLATE/gzip, JPEG; optimal prefix code
- [ ] `L3` Packing containers onto VMs is bin packing. What heuristic would you use? ↳ first-fit / best-fit decreasing; exact is NP-hard
- [ ] `L3` Greedy in load balancers and schedulers (least connections, shortest job first): what breaks?

## 4.18 Intervals
**Learn:** https://neetcode.io/roadmap (Intervals) · https://www.techinterviewhandbook.org/algorithms/interval/ · https://leetcode.com/problems/car-pooling/
- [ ] `L1` How do you check whether two intervals overlap in one line? ↳ a.start < b.end and b.start < a.end
- [ ] `L1` Why do most interval problems start by sorting? By start or by end?
- [ ] `L1` **Meeting Rooms** (LC 252, premium; free on neetcode.io) — can one person attend all meetings?
- [ ] `L2` **Merge Intervals** (LC 56) — then intervals arrive as a stream. ↳ sorted map / balanced tree; merge neighbours on insert
- [ ] `L2` **Insert Interval** (LC 57) in O(n) without re-sorting.
- [ ] `L2` **Non-overlapping Intervals** (LC 435) — why greedy by earliest end?
- [ ] `L2` **Meeting Rooms II** (LC 253, premium; free on neetcode.io) — min-heap of end times vs sweep line. ↳ +1/−1 events; process end before start on ties
- [ ] `L2` **Car Pooling** (LC 1094) — sweep line or difference array.
- [ ] `L2` **Interval List Intersections** (LC 986) — two pointers.
- [ ] `L2` **My Calendar I** (LC 729) — sorted list + bisect vs balanced tree.
- [ ] `L2` Inclusive vs exclusive end points: how do they change comparisons and tie-breaking?
- [ ] `L3` **Minimum Interval to Include Each Query** (LC 1851) — sort queries offline + min-heap. ↳ heap keyed by size; pop intervals ending before query
- [ ] `L3` Interval tree vs segment tree: which answers "all intervals overlapping point x"?
- [ ] `L3` Design room booking for 10k rooms with no double booking under concurrency. ↳ Postgres tstzrange + exclusion constraint (GiST)
- [ ] `L3` Where did you handle time ranges at work (reminders, schedules, slots), and how did you store them?

## 4.19 Math & Geometry
**Learn:** https://neetcode.io/roadmap (Math & Geometry) · https://cp-algorithms.com/algebra/binary-exp.html · https://cp-algorithms.com/algebra/euclid-algorithm.html · https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html
- [ ] `L1` **Plus One** (LC 66).
- [ ] `L1` **Happy Number** (LC 202) — why is this cycle detection? ↳ set, or Floyd on the digit-square sequence
- [ ] `L1` GCD with Euclid's algorithm, LCM from GCD — complexity? ↳ O(log min(a, b))
- [ ] `L1` Why do problems ask for answers mod 10⁹ + 7? ↳ avoid overflow; prime modulus allows modular inverses
- [ ] `L1` **Rotate Image** (LC 48) in place. ↳ transpose, then reverse each row
- [ ] `L1` **Spiral Matrix** (LC 54) — shrinking boundaries.
- [ ] `L1` **Set Matrix Zeroes** (LC 73) in O(1) space. ↳ first row/column as markers; extra flag for column 0
- [ ] `L2` **Pow(x, n)** (LC 50) — fast exponentiation; negative n; n = −2³¹. ↳ binary exponentiation O(log n); careful negating min int
- [ ] `L2` **Multiply Strings** (LC 43) — digit products land at positions i+j and i+j+1.
- [ ] `L2` **Detect Squares** (LC 2013) — count points; fix the diagonal corner.
- [ ] `L2` **Count Primes** (LC 204) — Sieve of Eratosthenes and its complexity. ↳ O(n log log n); start crossing out at p²
- [ ] `L2` **Shuffle an Array** (LC 384) — Fisher–Yates; why is swapping with any index biased? ↳ nⁿ outcomes aren't divisible by n!
- [ ] `L2` **Random Pick with Weight** (LC 528). ↳ prefix sums + binary search; alias method for O(1)
- [ ] `L2` Reservoir sampling: pick k items uniformly from a stream of unknown length. ↳ keep item i with probability k/i
- [ ] `L2` Why is `0.1 + 0.2 != 0.3`? How do you compare floats, and how do you store money? ↳ binary fractions; epsilon; integer paise or Decimal
- [ ] `L3` Matrix exponentiation for Fibonacci in O(log n). Modular inverse via Fermat for nCr mod p.
- [ ] `L3` "Restaurants within 2 km" (StreetDine): geohash vs quadtree vs H3. Why not Euclidean on lat/long? ↳ cells + neighbours, then haversine; PostGIS or Redis GEO

## 4.20 Bit Manipulation
**Learn:** https://neetcode.io/roadmap (Bit Manipulation) · https://www.techinterviewhandbook.org/algorithms/binary/ · https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number/MAX_SAFE_INTEGER · https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/BigInt
- [ ] `L1` What do AND, OR, XOR, NOT and the shifts do? Arithmetic vs logical right shift. ↳ JS `>>` keeps sign, `>>>` zero-fills
- [ ] `L1` What do `x & (x - 1)` and `x & -x` do? ↳ clear lowest set bit; isolate lowest set bit
- [ ] `L1` How do you check, set, clear and toggle bit i? How do you test for a power of two (LC 231)?
- [ ] `L1` What is two's complement? Why does `~x == -x - 1`?
- [ ] `L1` **Single Number** (LC 136) — why does XOR work?
- [ ] `L1` **Number of 1 Bits** (LC 191) — loop vs Brian Kernighan's trick.
- [ ] `L1` **Missing Number** (LC 268) — sum vs XOR, and the overflow concern.
- [ ] `L2` **Counting Bits** (LC 338) in O(n). ↳ dp[i] = dp[i >> 1] + (i & 1)
- [ ] `L2` **Reverse Bits** (LC 190) — then it is called millions of times. ↳ byte lookup table, or divide-and-conquer swaps
- [ ] `L2` **Sum of Two Integers** (LC 371) without `+` — and why Python needs a 32-bit mask. ↳ unbounded ints; mask 0xFFFFFFFF, restore sign
- [ ] `L2` **Reverse Integer** (LC 7) — detect 32-bit overflow before it happens.
- [ ] `L2` JS bitwise ops work on 32-bit ints and `Number.MAX_SAFE_INTEGER` is 2⁵³ − 1. When do you need `BigInt`? ↳ 64-bit IDs (Snowflake) lose precision in JSON
- [ ] `L2` **Single Number II** (LC 137) and **Single Number III** (LC 260).
- [ ] `L2` Iterate all submasks of a mask, and use bitmasks as DP state. ↳ sub = (sub − 1) & mask
- [ ] `L3` Where do bit flags appear in real systems? ↳ Unix permissions, feature flags, Bloom filters, Redis SETBIT/BITCOUNT
- [ ] `L3` Daily active users as a Redis bitmap: memory for 100M users? ↳ 100M bits ≈ 12.5 MB per day
- [ ] `L3` Snowflake IDs: how are the 64 bits split? ↳ sign, 41 time, 10 machine, 12 sequence

## 4.21 Sorting and selection
**Learn:** https://visualgo.net/en/sorting · https://docs.python.org/3/howto/sorting.html · https://v8.dev/blog/array-sort · https://en.wikipedia.org/wiki/Timsort · https://en.wikipedia.org/wiki/Quickselect · DDIA ch3 "SSTables and LSM-Trees" (pdf p96–99; mergesort-style merge)
- [ ] `L1` Compare insertion, selection, merge, quick and heap sort: best/average/worst time, extra space, stable?
- [ ] `L1` What is a stable sort? Give a case where stability matters. ↳ sort by name, then by city: equal cities keep name order
- [ ] `L1` Why is `[10, 9, 1].sort()` wrong in JS? ↳ default compares as strings; pass `(a, b) => a - b`
- [ ] `L1` Python `sort()` vs `sorted()`; `key=` vs `functools.cmp_to_key`.
- [ ] `L2` **Sort an Array** (LC 912) — write merge sort from memory.
- [ ] `L2` Write quicksort with Lomuto or Hoare partition. Why randomise the pivot? ↳ sorted input → O(n²); random pivot → expected n log n
- [ ] `L2` Quicksort on all-equal elements: what is 3-way partitioning? ↳ Dutch-flag partition into <, =, >
- [ ] `L2` Heap sort uses O(1) extra space — why is it slower than quicksort in practice? ↳ poor cache locality
- [ ] `L2` When is insertion sort the best choice? ↳ small or nearly sorted input; hybrids use it for short runs
- [ ] `L2` Counting, bucket and radix sort: when can you beat O(n log n)? Why must each radix pass be stable? ↳ bounded integer keys, fixed-width digits
- [ ] `L2` What sort does Python use? What does V8 use for `Array.prototype.sort`? ↳ Timsort in both (V8 since v7.0); stable
- [ ] `L2` How does Timsort work? ↳ find natural runs, extend with insertion sort, merge with galloping
- [ ] `L2` Quickselect for the k-th smallest — average and worst case; what does median-of-medians add? ↳ O(n) average, O(n²) worst; MoM guarantees O(n)
- [ ] `L2` **Largest Number** (LC 179) — the custom comparator. ↳ order a before b if a+b > b+a
- [ ] `L2` Count inversions in an array with merge sort.
- [ ] `L3` Sort 100 GB on a machine with 4 GB of RAM. ↳ sorted runs to disk, then k-way heap merge
- [ ] `L3` How does Postgres sort for `ORDER BY` when data exceeds `work_mem`, and how can an index avoid the sort? ↳ external merge to temp files
- [ ] `L3` What did Python 3.11 change in `list.sort`'s merge policy? ↳ switched to Powersort's merge ordering
- [ ] `L3` What is introsort, and who uses it? ↳ quicksort → heapsort at depth limit; C++ std::sort

## 4.22 Hashing internals
**Learn:** https://visualgo.net/en/hashtable · DDIA ch3 "Hash indexes" (pdf p92–96) · https://v8.dev/blog/fast-properties · https://v8.dev/blog/hash-code · Raymond Hettinger "Modern Python Dictionaries" (PyCon 2017) · https://github.com/python/cpython/blob/main/Objects/dictobject.c
- [ ] `L1` What is a hash function, and what makes one good for a hash table? ↳ fast, deterministic, uniform, small input change → big output change
- [ ] `L1` What is a collision, and why are collisions unavoidable? ↳ pigeonhole principle
- [ ] `L1` Chaining vs open addressing.
- [ ] `L1` What is the load factor, and what happens when it gets too high?
- [ ] `L1` Why must dict keys be hashable / immutable in Python? What breaks if you mutate a key? ↳ hash changes → lookup probes the wrong slot
- [ ] `L2` Linear probing vs quadratic probing vs double hashing: clustering trade-offs.
- [ ] `L2` How does deletion work in open addressing? ↳ tombstones; they slow lookups until the next resize
- [ ] `L2` How does resizing work, and why is insert still O(1) amortised? Why power-of-two sizes? ↳ rehash everything on doubling; bitmask instead of mod
- [ ] `L2` How does a Python `dict` work inside, and why is it insertion-ordered since 3.7? ↳ sparse index table + compact entries array; open addressing, perturbed probing
- [ ] `L2` When does a Python dict resize? ↳ when about two-thirds full
- [ ] `L2` JS `Map` vs plain object: key types, ordering, performance, prototype pitfalls.
- [ ] `L2` What are V8 hidden classes (shapes) and inline caches? Why does property order matter? ↳ same shape → monomorphic fast path; many shapes → megamorphic
- [ ] `L2` When does a V8 object drop into dictionary mode? ↳ deleting properties, many dynamically added properties
- [ ] `L2` The `__hash__` / `__eq__` contract in Python. What happens if you define only `__eq__`? ↳ equal → equal hashes; class becomes unhashable
- [ ] `L2` Why does `hash("abc")` change between Python runs? What is hash flooding (HashDoS)? ↳ randomised SipHash seed; crafted colliding keys
- [ ] `L2` Cryptographic vs non-cryptographic hashes: SHA-256 vs MurmurHash / xxHash / SipHash — when each?
- [ ] `L3` Robin Hood hashing, cuckoo hashing, Swiss tables: one line each. ↳ even out probe lengths; two tables, O(1) lookup; SIMD metadata groups
- [ ] `L3` Why does Java's `HashMap` turn a bucket into a tree at 8 entries? ↳ caps worst case at O(log n)
- [ ] `L3` How does Redis avoid a long pause when its hash table resizes? ↳ incremental rehash: two tables, move buckets per operation
- [ ] `L3` Postgres hash index vs B-tree index: why is the B-tree almost always chosen? ↳ no ranges or ordering; equality only

## 4.23 B-Trees and B+ Trees
**Learn:** DBI ch2 "Ubiquitous B-Trees" (pdf p69–85) · DBI ch3 "File Formats" · DBI ch4 "Implementing B-Trees" · DBI ch6 "B-Tree Variants" · DDIA ch3 "B-Trees" · https://www.postgresql.org/docs/current/btree.html
- [ ] `L1` What is a B-tree, and how is it different from a binary search tree? ↳ many keys per node, high fanout, leaves at equal depth
- [ ] `L1` B-tree vs B+ tree: where do values live, and why are leaves linked? ↳ B+: data only in leaves; sibling links for range scans
- [ ] `L1` What limits a node's fanout? How tall is a B+ tree over 1 billion rows? ↳ page size ÷ (key + pointer); 3–4 levels
- [ ] `L2` Walk through a lookup from root to leaf. How many disk reads? ↳ one page per level; upper levels usually cached
- [ ] `L2` Walk through an insert that splits a leaf, and a split that propagates to the root.
- [ ] `L2` What happens on delete? Merge vs redistribute, and why many databases skip merging. ↳ Postgres leaves half-empty pages to VACUUM/REINDEX
- [ ] `L2` Why a B+ tree and not a hash index for range queries and `ORDER BY`?
- [ ] `L2` Clustered vs secondary index: Postgres heap + TID vs InnoDB clustered primary key. ↳ InnoDB secondary entries store the primary key
- [ ] `L2` What is a covering index / index-only scan, and what does Postgres also need for it? ↳ visibility map
- [ ] `L2` Composite index `(a, b)`: which queries can use it, and why does column order matter? ↳ leftmost prefix; equality columns before range
- [ ] `L2` Why do random UUIDv4 primary keys hurt B-tree inserts, and what do UUIDv7 / ULID fix? ↳ random page splits, cache misses; time-ordered → right-edge appends
- [ ] `L2` What is a slotted page? ↳ header, cell-pointer array, cells grow from the end
- [ ] `L2` How does the database keep a B-tree consistent after a crash mid-split? ↳ WAL records page changes; redo on recovery
- [ ] `L2` Implement a B-tree insert with node splits in your language (minimum degree 2 is enough).
- [ ] `L3` What is a B-link tree (Lehman–Yao), and why does Postgres use it? ↳ right-links + high keys let readers survive concurrent splits
- [ ] `L3` Latch crabbing: how do concurrent B-tree operations stay safe?
- [ ] `L3` Copy-on-write B-trees (LMDB, Btrfs): what do they trade? ↳ no WAL, cheap snapshots; more write amplification
- [ ] `L3` Postgres index bloat: how does it happen and how do you fix it without downtime? ↳ REINDEX CONCURRENTLY, pg_repack
- [ ] `L3` Where did you add an index at work that changed the plan? How did you confirm it with `EXPLAIN ANALYZE`?

## 4.24 LSM trees
**Learn:** DBI ch7 "Log-Structured Storage" · DBI ch7 "Merge-Iteration" (pdf p232–236) · DDIA ch3 "SSTables and LSM-Trees" (pdf p96–99) · https://github.com/facebook/rocksdb/wiki/RocksDB-Overview
- [ ] `L1` What is an LSM tree in one sentence? ↳ buffer writes in memory, flush sorted immutable files, merge in background
- [ ] `L1` What are the memtable, the WAL and SSTables?
- [ ] `L1` Which databases use LSM trees, and why are their writes fast? ↳ RocksDB, LevelDB, Cassandra, ScyllaDB, HBase; sequential I/O
- [ ] `L2` Walk through a write: WAL append → memtable → flush to an SSTable.
- [ ] `L2` Walk through a point read. What makes it slow, and what helps? ↳ memtable, then SSTables newest first; Bloom filters, sparse index
- [ ] `L2` What data structure is the memtable usually built on? ↳ skip list in LevelDB and RocksDB
- [ ] `L2` How is a delete done? ↳ tombstone; physically removed during compaction
- [ ] `L2` What is compaction, and why is it needed? ↳ merge files, drop overwritten/deleted keys, bound read cost
- [ ] `L2` Size-tiered vs leveled compaction: trade-offs. ↳ tiered: less write amp, more space/read amp; leveled: opposite
- [ ] `L2` Define read, write and space amplification. ↳ RUM trade-off: can't minimise all three
- [ ] `L2` What is inside an SSTable besides the data? ↳ block index, Bloom filter, compressed blocks, footer
- [ ] `L2` Why are range scans costlier on an LSM tree than on a B-tree?
- [ ] `L3` Tombstones pile up in Cassandra. What goes wrong and how do you fix it? ↳ slow reads, query failures; gc_grace, compaction, data model change
- [ ] `L3` Compaction falls behind the write rate. Symptoms and fixes. ↳ write stalls, growing L0; more compaction threads, throttle writes
- [ ] `L3` What is key-value separation (WiscKey / BlobDB), and why? ↳ big values outside the tree → less write amplification
- [ ] `L3` List the pieces of a toy LSM key-value store you could build in a weekend.

## 4.25 Skip lists
**Learn:** DBI ch7 "Skiplist" (pdf p249–252) · William Pugh, "Skip Lists: A Probabilistic Alternative to Balanced Trees" (1990) · https://redis.io/docs/latest/develop/data-types/sorted-sets/ · https://leetcode.com/problems/design-skiplist/
- [ ] `L1` What is a skip list? Draw one. ↳ sorted linked list with randomly promoted express lanes
- [ ] `L1` Expected and worst-case cost of search, insert and delete? ↳ O(log n) expected; O(n) worst
- [ ] `L1` How is a new node's level chosen? ↳ repeated coin flips with probability p, capped at a max level
- [ ] `L2` **Design Skiplist** (LC 1206) — implement search, add and erase.
- [ ] `L2` Expected pointers per node with p = 1/2 vs p = 1/4. ↳ 1/(1−p): 2 vs about 1.33
- [ ] `L2` Skip list vs balanced BST: why might you prefer the skip list? ↳ simpler code, easy range iteration, simpler concurrency
- [ ] `L2` Skip list vs B-tree: why B-trees on disk but skip lists in memory?
- [ ] `L2` How does Redis implement a sorted set? ↳ hash table member→score + skip list by score; listpack when small
- [ ] `L2` How does Redis answer `ZRANK` in O(log n)? ↳ each forward pointer stores a span count
- [ ] `L2` Why did Redis choose a skip list over a balanced tree? ↳ simpler, fast range ops, tunable memory
- [ ] `L2` Build a game leaderboard with Redis sorted sets: top 10, a user's rank, users around me. ↳ ZADD, ZREVRANGE, ZREVRANK; ties via composite score
- [ ] `L3` Why are lock-free skip lists easier than lock-free balanced trees? ↳ local CAS updates, no rebalancing; Java ConcurrentSkipListMap
- [ ] `L3` A leaderboard for 100M players doesn't fit one Redis node. What now? ↳ shard by score range, approximate rank buckets
- [ ] `L3` How does `ZRANGEBYSCORE` turn a sorted set into a delay queue for reminders (AiRA)? ↳ score = due time; claim ≤ now atomically with Lua
- [ ] `L3` Where else is a skip list used as a core structure? ↳ LevelDB/RocksDB memtables, Lucene skip data, MemSQL indexes

## 4.26 Bloom filters
**Learn:** DBI ch7 "Bloom Filters" (pdf p246–249) · https://llimllib.github.io/bloomfilter-tutorial/ · https://redis.io/docs/latest/develop/data-types/probabilistic/bloom-filter/
- [ ] `L1` What is a Bloom filter, and what question does it answer? ↳ "definitely not present" or "probably present"
- [ ] `L1` Can it give false negatives? False positives?
- [ ] `L1` How do insert and lookup work with k hash functions over m bits?
- [ ] `L1` Can you delete from a Bloom filter? ↳ no; use a counting Bloom filter or cuckoo filter
- [ ] `L2` What controls the false-positive rate? Bits per element for about 1%? ↳ m/n and k; ~10 bits/element, k ≈ 7
- [ ] `L2` What is the optimal number of hash functions? ↳ k = (m/n)·ln 2
- [ ] `L2` How do you get k hash functions cheaply? ↳ double hashing: h1 + i·h2
- [ ] `L2` What happens when you insert far more items than planned? ↳ FPR climbs toward 1; scalable Bloom filters add layers
- [ ] `L2` Implement a Bloom filter over a `bytearray` / `Uint8Array`.
- [ ] `L2` How do LSM databases use Bloom filters, and what do they save? ↳ skip SSTables without the key; fewer disk reads
- [ ] `L2` Where else are Bloom filters used? ↳ Cassandra, Postgres bloom extension, CDNs, Medium recommendations, Bitcoin SPV
- [ ] `L2` Counting Bloom filter vs cuckoo filter: what does each add? ↳ deletion; cuckoo is also smaller at low FPR
- [ ] `L2` Design a "username taken?" check for 1B usernames with a Bloom filter in front of the database.
- [ ] `L3` How do you union two Bloom filters? Can you intersect them? ↳ same m, k, hashes: OR for union; AND approximates
- [ ] `L3` How would you dedupe events with Redis `BF.ADD` / `BF.EXISTS`, and what does a false positive cost you?

## 4.27 Count-Min Sketch
**Learn:** *Mining of Massive Datasets* ch4 "Mining Data Streams" (mmds.org) · Cormode & Muthukrishnan, "An Improved Data Stream Summary: The Count-Min Sketch" (2005) · https://redis.io/docs/latest/develop/data-types/probabilistic/count-min-sketch/
- [ ] `L1` What is a Count-Min Sketch, and what does it estimate? ↳ approximate frequency of each item in a stream
- [ ] `L1` How do update and query work? ↳ d rows × w counters; increment one per row; query takes the min
- [ ] `L1` Does it over-estimate or under-estimate, and why? ↳ only over-estimates; collisions only add
- [ ] `L2` How do width and depth relate to error and confidence? ↳ w ≈ e/ε, d ≈ ln(1/δ)
- [ ] `L2` Memory of a CMS vs an exact hash map of counts for 1B distinct keys.
- [ ] `L2` Count-Min Sketch vs Bloom filter: what is similar, what is different?
- [ ] `L2` Find top-K heavy hitters with a CMS. ↳ CMS for counts + min-heap of candidates
- [ ] `L2` What is conservative update, and why does it reduce error? ↳ raise only counters below the new estimate
- [ ] `L2` Can a CMS handle decrements? ↳ yes if true counts stay non-negative
- [ ] `L2` Merge sketches from two servers. ↳ same dimensions and hashes: add cell by cell
- [ ] `L2` Implement a Count-Min Sketch in about 20 lines.
- [ ] `L3` Count Sketch vs Count-Min Sketch: what do the ±1 hashes buy you? ↳ unbiased estimates; median of rows
- [ ] `L3` Detect abusive IPs at 1M requests/second: CMS or exact counters? ↳ CMS per window + threshold; exact counts for flagged keys
- [ ] `L3` Sliding-window counts with sketches: how do you expire old data? ↳ ring of per-minute sketches; sum the recent ones
- [ ] `L3` Where could a CMS help in an LLM gateway (per-tenant token usage, hot prompts)?

## 4.28 HyperLogLog
**Learn:** https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/ · Flajolet et al., "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm" (2007) · Heule et al., "HyperLogLog in Practice" (Google, 2013) · http://antirez.com/news/75
- [ ] `L1` What problem does HyperLogLog solve? ↳ approximate count-distinct in small fixed memory
- [ ] `L1` Exact count-distinct of 1B items with a hash set: roughly how much memory? ↳ tens of GB
- [ ] `L1` What do Redis `PFADD`, `PFCOUNT` and `PFMERGE` do?
- [ ] `L2` Why do leading zeros in a hash say something about cardinality? ↳ k leading zeros suggests ~2^k distinct values
- [ ] `L2` Why split into m registers and combine with a harmonic mean? ↳ cuts variance; harmonic mean damps outliers
- [ ] `L2` How much memory does a Redis HLL use, and what is its standard error? ↳ 12 KB; about 0.81%
- [ ] `L2` Standard error as a function of the register count. ↳ ≈ 1.04/√m
- [ ] `L2` How do you merge two HLLs, and why is that powerful? ↳ register-wise max; union across days or shards
- [ ] `L2` Can you intersect HLLs? ↳ only via inclusion–exclusion; error grows fast
- [ ] `L2` Why does HLL need a small-range correction? ↳ many empty registers → switch to linear counting
- [ ] `L2` Sparse vs dense encoding in Redis HLL.
- [ ] `L2` HLL vs Bloom filter vs Count-Min Sketch: which question does each answer? ↳ how many distinct; is x present; how often x
- [ ] `L3` Design daily, weekly and monthly unique visitors for 100M users. ↳ HLL per day; PFMERGE for week and month
- [ ] `L3` Postgres `count(DISTINCT)` is slow on a big table. Options? ↳ postgresql-hll extension, pre-aggregation, approximate answers
- [ ] `L3` Count unique active users per tenant per day in an AI product cheaply.

## 4.29 Consistent hashing
**Learn:** DDIA ch6 "Partitioning" (pdf p209–231) · DeCandia et al., "Dynamo: Amazon's Highly Available Key-value Store" (2007) §4.2 · Lamping & Veach, "A Fast, Minimal Memory, Consistent Hash Algorithm" (2014) · https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/
- [ ] `L1` What problem does consistent hashing solve? ↳ adding/removing a node moves only ~1/N of keys
- [ ] `L1` Describe the hash ring: where do nodes and keys go, and how does a key find its node?
- [ ] `L1` With `hash % N`, what fraction of keys move when N goes from 10 to 11? With a ring? ↳ ~91% vs ~9%
- [ ] `L2` What are virtual nodes, and why do you need them? ↳ even load, gradual rebalancing, weight by capacity
- [ ] `L2` How many virtual nodes per server, and what does too many cost? ↳ ring memory, slower lookups, more metadata
- [ ] `L2` Implement a ring with a sorted array of tokens + binary search. ↳ bisect for first token ≥ hash; wrap around
- [ ] `L2` How does replication work on the ring? ↳ preference list: next N distinct physical nodes clockwise
- [ ] `L2` Which systems use consistent hashing? ↳ Dynamo, Cassandra, Riak, ketama memcached clients, Envoy ring hash
- [ ] `L2` Redis Cluster does not use a ring. What does it use, and why? ↳ 16384 hash slots via CRC16; explicit slot migration
- [ ] `L2` Fixed partitions (hash slots) vs a consistent-hash ring: trade-offs.
- [ ] `L2` One hot key still overloads a node on a perfect ring. What do you do? ↳ replicate hot keys, salt the key, local cache
- [ ] `L3` Rendezvous (highest random weight) hashing vs ring hashing. ↳ score every node per key; no ring; O(N) lookup
- [ ] `L3` Jump consistent hash: strengths and limits. ↳ tiny, fast, balanced; buckets only added/removed at end
- [ ] `L3` Consistent hashing with bounded loads, and Maglev lookup tables in load balancers: what do they fix?
- [ ] `L3` Cache LLM responses by prompt hash across 20 nodes. Add a node without a stampede. ↳ ring with vnodes, warm-up, request coalescing

## 4.30 Merkle trees
**Learn:** DeCandia et al., "Dynamo" (2007) §4.7 "Handling permanent failures: Replica synchronization" · DBI ch12 "Anti-Entropy and Dissemination" · https://git-scm.com/book/en/v2/Git-Internals-Git-Objects · https://certificate.transparency.dev/howctworks/
- [ ] `L1` What is a Merkle tree? ↳ leaves hash data blocks; parents hash children; root summarises all
- [ ] `L1` What does comparing two Merkle roots tell you?
- [ ] `L1` How many hashes prove that one leaf belongs to a tree of n leaves? ↳ O(log n) sibling hashes
- [ ] `L2` How do Dynamo and Cassandra use Merkle trees for anti-entropy repair? ↳ compare per-range trees top-down; sync only differing ranges
- [ ] `L2` What does building Merkle trees cost during Cassandra repair, and why does incremental repair exist?
- [ ] `L2` Is a Git repository a Merkle tree? How does Git know two directories are identical instantly? ↳ Merkle DAG of blobs, trees, commits; equal hashes
- [ ] `L2` What does a blockchain light client verify with a Merkle proof? ↳ transaction inclusion against the block header root
- [ ] `L2` Certificate Transparency logs: what do inclusion and consistency proofs show?
- [ ] `L2` Implement a Merkle tree over a list of chunks and produce an inclusion proof.
- [ ] `L2` Sync a folder between laptop and server efficiently (Dropbox / rsync style). ↳ chunk + hash; tree of hashes finds changed chunks
- [ ] `L2` Odd number of leaves: what do implementations do, and why can that be a bug? ↳ duplicate last leaf; Bitcoin CVE-2012-2459
- [ ] `L3` Second-preimage attacks: why hash leaves and internal nodes differently? ↳ domain separation prefixes 0x00 / 0x01
- [ ] `L3` How do BitTorrent and IPFS verify content fetched from untrusted peers?
- [ ] `L3` Two replicas of a 1-billion-row table may have drifted. How do you find the differing rows without shipping all data?
- [ ] `L3` How could a Merkle tree help prove a RAG index still matches its source documents?

## 4.31 Ring buffers
**Learn:** https://lmax-exchange.github.io/disruptor/ · https://en.wikipedia.org/wiki/Circular_buffer · https://kernel.dk/io_uring.pdf · https://docs.python.org/3/library/collections.html#collections.deque
- [ ] `L1` What is a ring (circular) buffer? ↳ fixed array; head and tail indices wrap around
- [ ] `L1` How do you tell "full" from "empty"? ↳ keep a count, leave one slot empty, or monotonic counters
- [ ] `L1` What happens on write when it is full? Name two policies. ↳ overwrite oldest (logs, metrics) or block/reject (queues)
- [ ] `L2` **Design Circular Queue** (LC 622) — implement it.
- [ ] `L2` **Design Circular Deque** (LC 641).
- [ ] `L2` Why use a power-of-two capacity? ↳ `i & (size − 1)` instead of modulo
- [ ] `L2` What does Python's `deque(maxlen=n)` give you for free?
- [ ] `L2` Keep the last 1,000 log lines or request latencies: ring buffer vs list. ↳ O(1) append, fixed memory, no shifting
- [ ] `L2` Moving average over the last N values in O(1) per update.
- [ ] `L2` Where are ring buffers used in real systems? ↳ kernel log, io_uring SQ/CQ, NIC queues, audio, perf
- [ ] `L2` Why does a single-producer single-consumer ring buffer work without locks? ↳ each index written by one side; memory barriers
- [ ] `L3` Why is the LMAX Disruptor fast? ↳ preallocated ring, no locks, sequence counters, cache-line padding
- [ ] `L3` What is false sharing, and why pad head and tail onto separate cache lines?
- [ ] `L3` Why are multi-producer ring buffers harder? ↳ CAS on tail; publish order; per-slot sequence
- [ ] `L3` Where would a ring buffer fit in a realtime voice pipeline (audio frames, jitter buffer)?

## 4.32 HNSW and vector search
**Learn:** Malkov & Yashunin, "Efficient and robust approximate nearest neighbor search using Hierarchical Navigable Small World graphs" (https://arxiv.org/abs/1603.09320) · https://qdrant.tech/documentation/concepts/indexing/ · https://www.pinecone.io/learn/series/faiss/hnsw/ · https://github.com/pgvector/pgvector
- [ ] `L1` What is nearest-neighbour search on vectors, and why is exact search slow at scale? ↳ brute force is O(n·d) per query
- [ ] `L1` What does "approximate" in ANN mean? What is recall@k?
- [ ] `L1` What is HNSW in one sentence? ↳ layered proximity graph; greedy search from sparse top layer down
- [ ] `L1` Cosine vs dot product vs Euclidean: when do they rank the same? ↳ on normalised vectors
- [ ] `L2` How does an HNSW search move through the layers? ↳ greedy descent above; beam search of width ef at layer 0
- [ ] `L2` How is a node's top layer chosen, and why is that like a skip list? ↳ exponentially decaying random level
- [ ] `L2` What do `M`, `ef_construct` and `ef` control? ↳ links per node; build quality; query recall vs latency
- [ ] `L2` Estimate memory for 10M vectors of 1536 float32 dims plus the graph. ↳ ~61 GB of vectors + M links per node
- [ ] `L2` HNSW vs IVF vs flat index vs product quantisation: trade-offs.
- [ ] `L2` Why is deleting from HNSW hard? ↳ tombstones; connectivity degrades; periodic rebuild
- [ ] `L2` How does a filter like `tenant_id = X` interact with HNSW? ↳ strict filters break graph walks; payload index, filter-aware search
- [ ] `L2` Scalar, product and binary quantisation: memory saved vs recall lost. ↳ rescore top candidates with full vectors
- [ ] `L2` pgvector HNSW vs IVFFlat: when is Postgres enough?
- [ ] `L3` How did you tune Qdrant at AiRA? Which parameters, and how did you measure recall vs latency?
- [ ] `L3` Multi-tenant vector search: one collection with a tenant filter vs one collection per tenant.
- [ ] `L3` How do you evaluate a vector index offline? ↳ brute-force ground truth; recall@k vs QPS curve

## 4.33 LRU and LFU caches
**Learn:** https://neetcode.io/roadmap (LRU Cache) · DBI ch5 "FIFO and LRU" (pdf p151–152) · https://redis.io/docs/latest/develop/reference/eviction/ · https://docs.python.org/3/library/functools.html#functools.lru_cache
- [ ] `L1` Name five cache eviction policies. ↳ LRU, LFU, FIFO, random, TTL; also CLOCK, ARC
- [ ] `L1` LRU vs LFU: what does each keep?
- [ ] `L1` **LRU Cache** (LC 146) — `get` and `put` in O(1). ↳ hash map + doubly linked list
- [ ] `L2` Why a doubly linked list and not a singly linked one?
- [ ] `L2` LRU with Python `OrderedDict` and with a JS `Map`. ↳ move_to_end / popitem(last=False); Map delete + set
- [ ] `L2` **LFU Cache** (LC 460) in O(1). ↳ key → node, freq → list, track minFreq
- [ ] `L2` LFU's "old popular items never leave" problem. ↳ decay or aging of counters
- [ ] `L2` Add TTL to your LRU cache. Lazy vs active expiry? ↳ check on get; background sweep or expiry heap
- [ ] `L2` Make the LRU cache thread-safe. Where is the bottleneck? ↳ every get mutates order → one lock; shard it
- [ ] `L2` How does Redis do LRU, and why approximate? ↳ sample keys, evict oldest; 24-bit clock per object
- [ ] `L2` Redis `allkeys-lru` vs `volatile-lru` vs `allkeys-lfu` vs `noeviction`: which for a cache, which for sessions?
- [ ] `L2` What is CLOCK (second chance), and why does the Postgres buffer manager use clock sweep? ↳ approximate LRU without list moves on hit
- [ ] `L2` What is a cache stampede, and how do you prevent it? ↳ request coalescing, lock, jittered TTL, early refresh
- [ ] `L2` `functools.lru_cache` on an instance method: what leak can it cause? ↳ cache holds `self`; instances never freed
- [ ] `L3` ARC, 2Q, W-TinyLFU: why does Caffeine use W-TinyLFU? ↳ scan resistance; frequency-sketch admission filter
- [ ] `L3` A sequential scan flushes your LRU cache. How do databases protect against that? ↳ Postgres ring buffers for big scans; InnoDB midpoint insertion
- [ ] `L3` Which cache did you use at AiRA, what eviction policy, and what hit ratio?

## 4.34 Segment trees, Fenwick trees and ordered maps
**Learn:** https://cp-algorithms.com/data_structures/segment_tree.html · https://cp-algorithms.com/data_structures/fenwick.html · https://grantjenks.com/docs/sortedcontainers/ · DBI ch7 "Skiplist" (pdf p249–252) · https://leetcode.com/problems/range-sum-query-mutable/
- [ ] `L1` Range sums with no updates: what do you use? **Range Sum Query – Immutable** (LC 303). ↳ prefix sums, O(1) per query
- [ ] `L1` What is a segment tree, and what does each node store?
- [ ] `L1` What is a Fenwick (binary indexed) tree?
- [ ] `L2` **Range Sum Query – Mutable** (LC 307) — prefix sums vs sqrt decomposition vs Fenwick vs segment tree.
- [ ] `L2` Segment tree costs: build, point update, range query, memory. ↳ O(n), O(log n), O(log n); ~4n array
- [ ] `L2` How does `i & -i` drive Fenwick update and query?
- [ ] `L2` What can a segment tree do that a Fenwick tree can't easily? ↳ min/max, non-invertible ops, lazy range updates
- [ ] `L2` What is lazy propagation?
- [ ] `L2` **Count of Smaller Numbers After Self** (LC 315) — Fenwick + coordinate compression, or merge sort.
- [ ] `L2` What is an ordered map (TreeMap)? Python and JS have none built in — what do you use? ↳ sortedcontainers; bisect on a list; hand-written treap
- [ ] `L2` How is `sortedcontainers.SortedList` O(log n) without a tree? ↳ list of sorted sublists + bisect
- [ ] `L2` **Range Sum Query 2D – Immutable** (LC 304) — 2-D prefix sums and inclusion–exclusion.
- [ ] `L3` **The Skyline Problem** (LC 218) — sweep line with a max-heap or ordered map.
- [ ] `L3` Sparse table for range-minimum queries: O(1) queries, but no updates. Why?
- [ ] `L3` Where do range-aggregation trees appear in real systems? ↳ time-series rollups, order-book depth, leaderboards, monitoring

## 4.35 Design-a-data-structure round (rate limiter, hit counter, timers)
**Learn:** https://leetcode.com/tag/design/ · https://neetcode.io/practice · *System Design Interview* (Alex Xu) vol.1 ch4 "Design a Rate Limiter" · https://redis.io/glossary/rate-limiting/
- [ ] `L1` **Insert Delete GetRandom O(1)** (LC 380) — why an array plus a hash map? ↳ swap with last element before pop
- [ ] `L1` **Design Hit Counter** (LC 362, premium) — hits in the last 5 minutes. ↳ queue of timestamps, or 300-slot circular array
- [ ] `L2` Hit counter at 1M hits per second: what changes? ↳ per-second buckets in a ring; per-thread counters merged
- [ ] `L2` Rate limiter algorithms: fixed window, sliding log, sliding window counter, token bucket, leaky bucket. ↳ burst handling, memory, accuracy at window edges
- [ ] `L2` Implement a sliding-window-log rate limiter per user. Memory per user? ↳ deque of timestamps; O(limit)
- [ ] `L2` Implement a sliding-window-counter limiter. Why is the weighted previous window a good approximation?
- [ ] `L2` Make your rate limiter work across 10 API servers with Redis. ↳ INCR + EXPIRE, or sorted set in a Lua script
- [ ] `L2` **Insert Delete GetRandom O(1) – Duplicates allowed** (LC 381).
- [ ] `L2` **Snapshot Array** (LC 1146). ↳ per-index list of (snap_id, value) + binary search
- [ ] `L2` **Design Browser History** (LC 1472) and **Design Underground System** (LC 1396).
- [ ] `L2` **All O'one Data Structure** (LC 432) — inc, dec, getMax, getMin all O(1).
- [ ] `L2` **Maximum Frequency Stack** (LC 895).
- [ ] `L2` **Design Snake Game** (LC 353, premium) — deque + set of occupied cells.
- [ ] `L2` **Design In-Memory File System** (LC 588, premium) — a trie of path parts.
- [ ] `L2` Design a key-value store with `set`, `get` and nested `begin` / `commit` / `rollback`. ↳ stack of change logs; common machine-coding prompt
- [ ] `L3` Design undo/redo for a text editor. ↳ two command stacks; rope or piece table for text
- [ ] `L3` Design a job scheduler: `schedule(job, at)`, `cancel(id)`, run due jobs. ↳ min-heap + id map, lazy cancel
- [ ] `L3` Hierarchical timing wheels: why do Kafka and Netty use them instead of a heap? ↳ O(1) insert/cancel for huge timer counts
- [ ] `L3` Write an in-memory cache class with LRU eviction, per-key TTL and a byte-size limit in 45 minutes.

## 4.36 DSA ↔ real systems mapping
**Learn:** DDIA ch3 "Storage and Retrieval" · DBI ch2–7 · syllabus "DSA ↔ Real Systems Mapping" (`../../syllabus.html`) · https://redis.io/docs/latest/develop/data-types/
- [ ] `L2` Where does a heap show up in a job scheduler, a rate limiter and a timer system?
- [ ] `L2` A `created_at` range query is fast but `LIKE '%term%'` is slow. Explain with data structures. ↳ B-tree needs a prefix; trigram GIN for infix
- [ ] `L2` Which data structures sit under each Redis type? ↳ SDS strings, quicklist lists, listpack/hashtable, intset, skiplist zsets
- [ ] `L2` What data structure is a Postgres WAL? A Kafka partition? ↳ append-only log
- [ ] `L2` What is an inverted index, and how do Elasticsearch and Postgres GIN use it? ↳ term → sorted posting list
- [ ] `L2` How do you intersect two sorted posting lists fast? ↳ two pointers; galloping; skip pointers
- [ ] `L2` What structures does a load balancer use for round robin, least connections and consistent hashing?
- [ ] `L2` How does an API gateway match URL paths quickly? ↳ radix tree
- [ ] `L2` Where are DAGs used in build systems, Airflow, Git history and LLM agent workflows?
- [ ] `L2` How does Git find the merge base of two branches? ↳ lowest common ancestor in the commit DAG
- [ ] `L2` How does a spreadsheet decide what to recalculate when a cell changes? ↳ dependency graph + topological order
- [ ] `L2` Explain mark-and-sweep garbage collection in graph terms. ↳ traverse from roots; unreached objects freed
- [ ] `L2` Which structure for "drivers near me"? ↳ geohash, quadtree, R-tree, H3; Redis GEO is a sorted set
- [ ] `L2` How does a time-series database store and compress points? ↳ columnar chunks, delta-of-delta timestamps, XOR floats (Gorilla)
- [ ] `L2` What does the OS use to map virtual to physical pages? ↳ multi-level page table (radix tree) + TLB
- [ ] `L2` Which queues and buffers sit inside Node's event loop and Linux networking?
- [ ] `L2` Which data structures did you rely on most in your last project, and which would you change now?
- [ ] `L3` Postgres B-tree vs hash vs GIN vs GiST vs BRIN: give one query for each.
- [ ] `L3` BRIN index: why is it tiny, and when does it work? ↳ min/max per block range; needs physical ordering, e.g. append-only time
- [ ] `L3` R-tree vs quadtree vs geohash for a ride-hailing app.
- [ ] `L3` How do CRDTs in collaborative editors relate to data structures? ↳ mergeable replicated sets, counters, sequences
- [ ] `L3` LLM agent memory: which structures for recent turns, semantic recall and entity facts? ↳ deque/ring buffer, vector index, key-value or graph

## 4.37 Concurrency-flavoured DSA
**Learn:** *The Little Book of Semaphores* (Allen Downey, free) · https://docs.python.org/3/library/queue.html · https://docs.python.org/3/library/asyncio-queue.html · https://docs.python.org/3/library/threading.html#condition-objects · https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics
- [ ] `L1` What is a race condition? Show one with `count += 1` across threads. ↳ read-modify-write isn't atomic
- [ ] `L1` Mutex vs semaphore vs condition variable.
- [ ] `L1` What is the producer–consumer problem?
- [ ] `L1` Is `list.append` thread-safe in CPython? Is `d[k] += 1`? ↳ single bytecode ops are atomic under GIL; += isn't
- [ ] `L1` Does Node.js need locks? When does it still have races? ↳ interleaving across `await`; worker threads + SharedArrayBuffer
- [ ] `L2` Implement a thread-safe bounded blocking queue with a lock and two condition variables. ↳ not_full / not_empty; wait inside a while loop
- [ ] `L2` Why `wait()` inside `while` and not `if`? ↳ spurious wakeups; another consumer took the item
- [ ] `L2` Implement the same bounded queue with two semaphores and a mutex.
- [ ] `L2` **Design Bounded Blocking Queue** (LC 1188, premium).
- [ ] `L2` `queue.Queue` vs `asyncio.Queue` vs `multiprocessing.Queue`: when each?
- [ ] `L2` Producer/consumer with `asyncio.Queue` and graceful shutdown. ↳ sentinels or `join()` + `task_done()`, then cancel workers
- [ ] `L2` Implement a token bucket rate limiter. What state do you store? ↳ tokens, last_refill; refill lazily on each call
- [ ] `L2` Make the token bucket thread-safe, then distributed with Redis. ↳ lock refill+take; atomic Lua script in Redis
- [ ] `L2` Token bucket vs leaky bucket: what does each allow? ↳ token permits bursts to capacity; leaky smooths output
- [ ] `L2` **Print in Order** (LC 1114) and **Print FooBar Alternately** (LC 1115) — events or semaphores.
- [ ] `L2` **The Dining Philosophers** (LC 1226) — how do you avoid deadlock? ↳ global lock order, limit diners, try-lock
- [ ] `L2` The four conditions for deadlock, and how to break each. ↳ mutual exclusion, hold-and-wait, no preemption, circular wait
- [ ] `L2` Implement a read-write lock. What is writer starvation?
- [ ] `L2` Implement a fixed-size thread pool with a task queue.
- [ ] `L2` Backpressure: what should a producer do when the bounded queue is full? ↳ block, drop, reject with 429, shed oldest
- [ ] `L2` What is compare-and-swap, and how does a lock-free (Treiber) stack use it?
- [ ] `L3` What is the ABA problem? ↳ A→B→A fools CAS; tagged pointers or hazard pointers
- [ ] `L3` A delayed-task queue consumed by many worker processes: how do you claim jobs safely? ↳ Redis ZSET + Lua claim, or Postgres SKIP LOCKED
- [ ] `L3` Implement a Redis distributed lock. What can still go wrong? ↳ SET NX PX + token; expiry during GC pause; fencing tokens
- [ ] `L3` How does Java's ConcurrentHashMap avoid a global lock? ↳ per-bin locks and CAS; lock-free reads
- [ ] `L3` Free-threaded Python (3.13+, no GIL): what changes for dicts, lists and your own structures?
- [ ] `L3` How did AiRA avoid sending the same reminder twice across workers? Which structure and lock?

## 4.38 Rapid-fire round
- [ ] `L1` Time complexity of binary search?
- [ ] `L1` Hash map lookup: average and worst case?
- [ ] `L1` Cost of heapify on n elements?
- [ ] `L1` Which of merge, quick and heap sort is stable?
- [ ] `L1` Which algorithm does Python's `sorted` use?
- [ ] `L1` BFS uses a ___; DFS uses a ___?
- [ ] `L1` Which BST traversal gives sorted order?
- [ ] `L1` Height of a balanced binary tree with n nodes?
- [ ] `L1` Maximum edges in a simple undirected graph with V nodes? ↳ V(V−1)/2
- [ ] `L1` Shortest path with non-negative weights: which algorithm?
- [ ] `L1` Name two ways to topologically sort.
- [ ] `L1` Floyd's algorithm uses which two pointers?
- [ ] `L1` XOR of a number with itself?
- [ ] `L1` Number of subsets of n elements? Permutations of n distinct elements?
- [ ] `L1` The two structures inside an LRU cache?
- [ ] `L1` Which structure orders a Redis sorted set?
- [ ] `L1` Memory of one Redis HyperLogLog?
- [ ] `L1` Python's default recursion limit?
- [ ] `L1` Value of `Number.MAX_SAFE_INTEGER`?
- [ ] `L1` Is `heapq` a min-heap or a max-heap?
- [ ] `L1` Time complexity of Kadane's algorithm?
- [ ] `L1` Quicksort's worst case, and when it happens?
- [ ] `L1` A monotonic stack finds what, in five words?
- [ ] `L1` Trie lookup cost for a word of length L?
- [ ] `L1` Amortised cost per Union-Find operation with both optimisations?
- [ ] `L1` What do B+ tree internal nodes store?
- [ ] `L1` An LSM memtable is usually which structure?
- [ ] `L1` Number of hash slots in Redis Cluster?
- [ ] `L1` Does a Bloom filter ever say "no" wrongly?
- [ ] `L1` Does a Count-Min Sketch under-count?
- [ ] `L1` Which direction does 0/1 knapsack loop over capacity?
- [ ] `L1` Which index does Qdrant use for vectors?
- [ ] `L1` What is a ring buffer's write cost?
- [ ] `L1` Best data structure for "next greater element"?
- [ ] `L1` O(1) membership test: which structure?
