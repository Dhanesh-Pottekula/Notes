# 7. JavaScript and TypeScript

Every Node.js/NestJS round starts with JavaScript fundamentals (coercion, closures, `this`, prototypes, "implement
`debounce`") and, for TypeScript shops, moves to the type system: narrowing, generics, conditional and mapped types,
and "how would you type this API?". A 3-year engineer must answer the JS core instantly, write small polyfills on a
whiteboard, and use TypeScript to model a domain (branded ids, discriminated unions, `Result` types), not just
annotate it. Syllabus: 1C TypeScript Deep Mastery (`../../syllabus.html`).

## 7.1 Types, values and coercion
**Learn:** `../../javascript/jsNotes.md` "Data Types", "Type Conversions" · https://javascript.info/types · https://javascript.info/type-conversions · https://javascript.info/comparison · *You Don't Know JS Yet* "Types & Grammar" (github.com/getify/You-Dont-Know-JS)
- [ ] `L1` Name the primitive types in JavaScript. ↳ string, number, bigint, boolean, undefined, null, symbol
- [ ] `L1` Is `Symbol` a primitive or an object? Is a function an object?
- [ ] `L1` `null` vs `undefined`: what does each mean, and when do you get each?
- [ ] `L1` What does `typeof null` return, and why? ↳ "object"; historical bug, never fixed
- [ ] `L1` What does `typeof` return for an array, a function, `NaN`, an undeclared variable?
- [ ] `L1` List all falsy values. ↳ false, 0, -0, 0n, "", null, undefined, NaN
- [ ] `L1` Are `[]` and `{}` truthy? What is `Boolean([])`?
- [ ] `L1` What does `!!value` do?
- [ ] `L1` `==` vs `===`: what is the difference?
- [ ] `L1` What is `NaN`? Why is `NaN === NaN` false? How do you check for it? ↳ `Number.isNaN`, `Object.is`
- [ ] `L1` What is the safe integer range of `Number`? What is `BigInt` for? ↳ ±(2^53 − 1); arbitrary-size integers
- [ ] `L2` What do `Number(undefined)`, `Number(null)`, `Number("")`, `Number("  123  ")`, `Number("12px")` return?
- [ ] `L2` Why is `null >= 0` true but `null == 0` false? ↳ comparisons convert to number; `==` treats null specially
- [ ] `L2` Why are `undefined > 0`, `undefined < 0` and `undefined == 0` all false?
- [ ] `L2` Why is `undefined == null` true but `undefined === null` false?
- [ ] `L2` `??` vs `||`: when do they give different results? ↳ `0`, `""`, `false` are kept by `??`
- [ ] `L2` Why is `0.1 + 0.2 !== 0.3`? How do you compare money safely? ↳ IEEE 754 binary floats; integers in paise/cents, decimal libs
- [ ] `L2` What do `"5" + 2`, `"5" - 2`, `true + 1`, `[] + []`, `[] + {}` evaluate to?
- [ ] `L2` Why is `[] == ![]` true? ↳ `![]` is false → 0; `[]` → "" → 0
- [ ] `L2` What does `[1, 2, 3].map(parseInt)` return, and why? ↳ parseInt gets index as radix: [1, NaN, NaN]
- [ ] `L2` What are `ToPrimitive`, `valueOf` and `toString` used for during coercion?
- [ ] `L2` What is `Object.is` and how does it differ from `===`? ↳ NaN equals NaN; +0 and −0 differ
- [ ] `L2` What is the difference between a primitive and its wrapper object (`"a"` vs `new String("a")`)?
- [ ] `L2` Can you mix `BigInt` and `Number` in arithmetic? What does `JSON.stringify(10n)` do? ↳ TypeError for both
- [ ] `L3` What is `Symbol.toPrimitive`, and how does it change `+obj` and template-string conversion?
- [ ] `L3` Why do 64-bit ids from a database (e.g. Twitter snowflake ids) break in JSON, and how do you fix it? ↳ above 2^53 precision lost; send as strings
- [ ] `L3` How does the `==` algorithm work, step by step, for object vs primitive?

## 7.2 Scope, hoisting, the TDZ and closures
**Learn:** https://javascript.info/var · https://javascript.info/closure · MDN "let" — "Temporal dead zone" and "Closures" (developer.mozilla.org) · *You Don't Know JS Yet* "Scope & Closures" (github.com/getify/You-Dont-Know-JS)
- [ ] `L1` `var` vs `let` vs `const`: three differences. ↳ function vs block scope, hoisting/TDZ, redeclaration/reassignment
- [ ] `L1` What is hoisting?
- [ ] `L1` What is the temporal dead zone (TDZ)?
- [ ] `L1` Does `const` make an object immutable?
- [ ] `L1` What is lexical scope?
- [ ] `L1` What is a closure? Explain with an example.
- [ ] `L1` Give three practical uses of closures. ↳ private state, factories/partial application, callbacks/handlers, memoize
- [ ] `L2` What prints? `console.log(a); var a = 1;` and then the same with `let`. ↳ undefined; ReferenceError
- [ ] `L2` Function declaration vs function expression vs arrow function: which are hoisted and how?
- [ ] `L2` What prints? `console.log(typeof x); let x = 1;` ↳ ReferenceError — `typeof` is not safe in the TDZ
- [ ] `L2` What is the scope chain?
- [ ] `L2` What is block scope, and how did `let` fix the classic loop bug?
- [ ] `L2` What creates an accidental global, and how does `"use strict"` stop it?
- [ ] `L2` What else does strict mode change? ↳ `this` undefined in plain calls, no silent failures, no `with`, no octal
- [ ] `L2` What is shadowing?
- [ ] `L2` What is an IIFE, and why was it used before modules?
- [ ] `L2` What prints? `for (var i = 0; i < 3; i++) setTimeout(() => console.log(i))` — and with `let`? ↳ 3 3 3; 0 1 2
- [ ] `L2` Fix the `var` loop bug three ways. ↳ `let`, IIFE, pass `i` as setTimeout third arg / bind
- [ ] `L2` Write a counter with private state using a closure.
- [ ] `L2` Write `once(fn)`.
- [ ] `L2` Write `memoize(fn)`. What is the key, and what is the memory risk?
- [ ] `L2` What is currying? Write `curry(fn)` for any number of arguments.
- [ ] `L2` What is partial application, and how does it differ from currying?
- [ ] `L2` Closures vs classes with private fields (`#x`): when do you use each?
- [ ] `L2` What is a stale closure? Give a backend example (a timer reading an old config value).
- [ ] `L3` Why does `let` in a `for` loop create a new binding per iteration, and what does the spec do to make that work?
- [ ] `L3` What happens with a function declaration inside a block in sloppy vs strict mode?
- [ ] `L3` What is the difference between the global object (`globalThis`) and the global lexical environment (`let` at top level)?
- [ ] `L3` How can a closure cause a memory leak? ↳ captures big object; long-lived callback keeps it alive
- [ ] `L3` Do closures capture variables or values? Show code that proves it.
- [ ] `L3` Implement the module pattern and explain what ES modules replaced.

## 7.3 `this`, `call`, `apply` and `bind`
**Learn:** https://javascript.info/object-methods · https://javascript.info/bind · https://javascript.info/arrow-functions · *You Don't Know JS Yet* "Objects & Classes" ("this")
- [ ] `L1` What is `this` in JavaScript?
- [ ] `L1` Name the four binding rules for `this`, in priority order. ↳ new > explicit (call/apply/bind) > implicit (obj.f()) > default
- [ ] `L1` `call` vs `apply` vs `bind`: difference?
- [ ] `L1` How is `this` different in an arrow function? ↳ lexical; taken from enclosing scope; cannot be rebound
- [ ] `L2` What is `this` in a plain function call in strict vs sloppy mode?
- [ ] `L2` Why does `const f = obj.method; f()` lose `this`? How do you fix it?
- [ ] `L2` What prints (CommonJS)? `const o = { n: 'a', f() { return () => this.n }, g: () => this.n }; console.log(o.f()(), o.g())`
- [ ] `L2` Why do class methods passed as callbacks (e.g. `emitter.on('x', this.handle)`) lose `this`? Two fixes.
- [ ] `L2` Can you re-`bind` a bound function? ↳ no; first bind wins (except with `new`)
- [ ] `L2` Implement `Function.prototype.bind`. ↳ return function, merge args, handle `new` and prototype
- [ ] `L2` Implement `call` and `apply` without using them. ↳ temporary Symbol property on the context
- [ ] `L2` What is `this` inside a `setTimeout` callback in Node?
- [ ] `L2` What is `this` at the top level of a CommonJS module vs an ES module? ↳ `module.exports` vs undefined
- [ ] `L3` Why are arrow functions bad as object methods and prototype methods?
- [ ] `L3` Arrow-function class fields (`handle = () => {}`) vs prototype methods: memory and inheritance trade-offs.

## 7.4 Prototypes, classes and `new`
**Learn:** https://javascript.info/prototype-inheritance · https://javascript.info/class · MDN "Inheritance and the prototype chain" (developer.mozilla.org)
- [ ] `L1` What is a prototype? What is the prototype chain?
- [ ] `L1` `__proto__` vs `prototype`: difference?
- [ ] `L1` Is `class` in JS real classes or sugar? ↳ sugar over prototypes, plus stricter semantics
- [ ] `L1` What does `new` do, step by step? ↳ create object, link prototype, call with `this`, return object unless object returned
- [ ] `L2` Implement `new` as a function (`myNew(Ctor, ...args)`).
- [ ] `L2` Implement `instanceof`.
- [ ] `L2` What does `Object.create(proto)` do? What is `Object.create(null)` good for? ↳ dictionary with no inherited keys like `__proto__`
- [ ] `L2` How do you do inheritance without `class` (constructor functions + prototypes)?
- [ ] `L2` What does `super` do in a constructor and in a method? Why must `super()` come before `this`?
- [ ] `L2` What are static methods and static blocks?
- [ ] `L2` Private fields (`#x`) vs TypeScript `private`: what is the difference at runtime? ↳ `#x` truly private; TS `private` is compile-time only
- [ ] `L2` Getters and setters: when are they useful, and what is the cost?
- [ ] `L2` Composition vs inheritance in JS: which do you prefer and why?
- [ ] `L2` What are mixins, and how do you write one?
- [ ] `L2` `hasOwnProperty` vs `in` vs `Object.hasOwn`.
- [ ] `L3` What is prototype pollution? How does `merge(target, JSON.parse(userInput))` cause it? ↳ `__proto__` key; block it, `Object.create(null)`, Map
- [ ] `L3` Why is changing an object's prototype at runtime bad for performance?
- [ ] `L3` How do you extend built-ins like `Error` or `Array` correctly, and what used to break with transpilers?

## 7.5 Objects, arrays, Map/Set, immutability and copying
**Learn:** https://javascript.info/object · https://javascript.info/array-methods · https://javascript.info/map-set · https://javascript.info/destructuring-assignment · MDN "structuredClone()" (developer.mozilla.org)
- [ ] `L1` Object vs `Map`: when do you use each? ↳ any key type, order, size, frequent add/delete, no prototype keys
- [ ] `L1` What is a `Set`? How do you dedupe an array?
- [ ] `L1` What is destructuring? Spread vs rest?
- [ ] `L1` What do optional chaining (`?.`) and nullish coalescing (`??`) do?
- [ ] `L1` `map` vs `forEach` vs `filter` vs `reduce` vs `flatMap`: what does each return?
- [ ] `L2` Shallow copy vs deep copy: give two ways to do each.
- [ ] `L2` What does `structuredClone` copy that `JSON.parse(JSON.stringify())` loses? ↳ Date, Map, Set, cycles, undefined; not functions or class prototypes
- [ ] `L2` `Object.freeze` vs `Object.seal` vs `Object.preventExtensions`. Is freeze deep?
- [ ] `L2` How do you update nested state immutably? Why care in backend code?
- [ ] `L2` Which array methods mutate and which return a new array? What are `toSorted`, `toReversed`, `with`?
- [ ] `L2` Why does `[10, 1, 2].sort()` give `[1, 10, 2]`? ↳ default sort compares strings
- [ ] `L2` What is the order of keys in an object? ↳ integer-like keys ascending, then strings in insertion order, then symbols
- [ ] `L2` `Object.keys` vs `Object.entries` vs `for…in` vs `Reflect.ownKeys`.
- [ ] `L2` What is `Object.groupBy` / `Map.groupBy`?
- [ ] `L2` What are WeakMap and WeakSet for, compared with Map and Set?
- [ ] `L2` What does `JSON.stringify` do with `undefined`, functions, `Date`, `NaN` and a `toJSON` method?
- [ ] `L2` How do you compare two objects for equality? Implement `deepEqual`.
- [ ] `L3` Implement `deepClone` that handles cycles, Date, Map and Set. ↳ WeakMap of seen objects
- [ ] `L3` What are property descriptors (`writable`, `enumerable`, `configurable`) and `Object.defineProperty`?
- [ ] `L3` Why might immutable updates of a 100k-element array in a hot path be a performance problem, and what do you do?

## 7.6 Modules — ES modules vs CommonJS, npm and packaging
**Learn:** https://javascript.info/modules-intro · https://nodejs.org/api/esm.html · https://nodejs.org/api/modules.html · https://nodejs.org/api/packages.html · https://docs.npmjs.com/about-semantic-versioning
- [ ] `L1` CommonJS vs ES modules: name four differences. ↳ require vs import, sync vs async load, dynamic vs static, live bindings
- [ ] `L1` How does Node decide whether a `.js` file is ESM or CJS? ↳ `"type"` in package.json, `.mjs`/`.cjs`
- [ ] `L1` What is a transpiler? What is a polyfill? How are they different? ↳ rewrites syntax vs adds missing runtime APIs
- [ ] `L1` What is `^1.2.3` vs `~1.2.3` vs `1.2.3` in package.json?
- [ ] `L1` What is `package-lock.json` for? `npm install` vs `npm ci`?
- [ ] `L2` What are "live bindings" in ESM, and how is that different from CJS `module.exports`?
- [ ] `L2` Can you `require` an ES module? Can you `import` a CommonJS module? What are the caveats? ↳ newer Node allows require(esm) without top-level await; named exports detection
- [ ] `L2` What is dynamic `import()` and when would you use it?
- [ ] `L2` How does `require` cache modules? What does it mean for singletons?
- [ ] `L2` What is a circular dependency? What happens in CJS vs ESM? ↳ CJS gets partial exports; ESM TDZ errors
- [ ] `L2` What is tree shaking, and why does it need ESM?
- [ ] `L2` What is the `exports` field in package.json, and what problem does it solve?
- [ ] `L2` dependencies vs devDependencies vs peerDependencies vs optionalDependencies.
- [ ] `L2` How do `__dirname` and `__filename` work in ESM? ↳ `import.meta.dirname` / `import.meta.url`
- [ ] `L2` What is the dual-package hazard?
- [ ] `L3` How does TypeScript's `module` / `moduleResolution` (`nodenext`, `bundler`) map onto Node's ESM/CJS rules?
- [ ] `L3` What is a supply-chain attack on npm, and how do you reduce the risk? ↳ lockfiles, `npm ci`, audit, pin, provenance, disable install scripts
- [ ] `L3` Why does `npm ci` fail when package.json and the lockfile disagree, and why is that good for CI?

## 7.7 Iterators, generators, Symbols, Proxy and Reflect
**Learn:** https://javascript.info/iterable · https://javascript.info/generators · https://javascript.info/async-iterators-generators · https://javascript.info/proxy · https://javascript.info/symbol
- [ ] `L1` What is the iterable protocol? The iterator protocol? ↳ `[Symbol.iterator]()` returns `{ next() }` → `{ value, done }`
- [ ] `L1` What is a generator function (`function*`)? What does `yield` do?
- [ ] `L1` What is a Symbol? Why use one as an object key?
- [ ] `L2` `for…of` vs `for…in`: what does each iterate?
- [ ] `L2` Make a custom class iterable.
- [ ] `L2` Write a generator that yields an infinite id sequence, and take the first 5.
- [ ] `L2` What do `gen.next(value)`, `gen.return()` and `gen.throw()` do?
- [ ] `L2` What is `yield*`?
- [ ] `L2` What is an async generator? Use one to page through an API that returns a cursor.
- [ ] `L2` How do you stream LLM tokens with `for await…of`, and how do you stop early? ↳ `break` calls `return()`; wire to AbortController
- [ ] `L2` What are well-known symbols? Name three. ↳ `Symbol.iterator`, `Symbol.asyncIterator`, `Symbol.toPrimitive`, `Symbol.hasInstance`
- [ ] `L2` `Symbol('x')` vs `Symbol.for('x')`.
- [ ] `L2` What is a `Proxy`? Name three traps.
- [ ] `L2` What is `Reflect`, and why use it inside Proxy traps?
- [ ] `L2` Give a real use of Proxy. ↳ validation, ORMs/lazy loading, observability, MobX/Vue reactivity, mocks
- [ ] `L3` Build a Proxy that logs every property read and throws on unknown keys.
- [ ] `L3` What is the performance cost of Proxy, and why should it stay out of hot paths?
- [ ] `L3` How do generators relate to async/await historically (co, regenerator)?
- [ ] `L3` What are iterator helpers (`.map`, `.filter`, `.take` on iterators), and why are they lazy?

## 7.8 Implement-it — polyfills and utilities
**Learn:** https://www.greatfrontend.com/questions (JavaScript coding) · https://bigfrontend.dev · https://javascript.info/call-apply-decorators
- [ ] `L2` Implement `debounce(fn, ms)`. ↳ clear previous timer, keep `this`/args, optional leading/cancel
- [ ] `L2` Implement `throttle(fn, ms)`. Debounce vs throttle — give a backend use for each.
- [ ] `L2` Implement `Array.prototype.map` (polyfill). ↳ handle `thisArg`, holes, don't mutate, index and array args
- [ ] `L2` Implement `Array.prototype.filter` and `Array.prototype.reduce` (with and without an initial value).
- [ ] `L2` Implement `Promise.all` as a polyfill.
- [ ] `L2` Implement `flatten(arr, depth)` without `.flat()`.
- [ ] `L2` Implement `get(obj, 'a.b[0].c', defaultValue)`.
- [ ] `L2` Implement a tiny EventEmitter (`on`, `off`, `once`, `emit`).
- [ ] `L2` Implement an LRU cache with O(1) `get` and `put`. ↳ Map keeps insertion order: delete then re-set
- [ ] `L2` Implement `pipe` and `compose`.
- [ ] `L2` Implement `groupBy(arr, keyFn)` and `chunk(arr, size)`.
- [ ] `L3` Implement a minimal `Promise` class (then, catch, resolve chaining). ↳ states, handler queue, async via microtask, thenable adoption
- [ ] `L3` Implement `deepFreeze`.
- [ ] `L3` Implement `debounce` that returns a promise resolving with the last call's result.
- [ ] `L3` Implement a retry-with-timeout wrapper that keeps the original function's TypeScript types.
- [ ] `L3` Implement `asyncPool(limit, items, fn)` and type it.

## 7.9 TypeScript basics — structural typing and the core types
**Learn:** https://www.typescriptlang.org/docs/handbook/2/everyday-types.html · https://www.typescriptlang.org/docs/handbook/type-compatibility.html · *Effective TypeScript* (2nd ed) ch.1 "Getting to Know TypeScript", ch.2 "TypeScript's Type System"
- [ ] `L1` Why TypeScript? What does it give you, and what does it not give you at runtime?
- [ ] `L1` What is structural typing ("duck typing at compile time")? How is it different from nominal typing (Java)?
- [ ] `L1` `type` vs `interface`: differences, and which do you default to? ↳ merging, extends vs &, unions only with type
- [ ] `L1` `any` vs `unknown`: which is safer and why?
- [ ] `L1` What is `never`? Give two places it appears.
- [ ] `L1` What is `void`? `void` vs `undefined` as a return type?
- [ ] `L1` What is a literal type? What is a union type? What is an intersection type?
- [ ] `L1` What is type inference? When should you write annotations anyway?
- [ ] `L2` What is an excess property check, and why does it fire for an object literal but not a variable?
- [ ] `L2` Optional property (`x?: T`) vs `x: T | undefined`: is there a difference? ↳ with `exactOptionalPropertyTypes`, yes
- [ ] `L2` What is type widening? Why does `let x = 'a'` have type `string` but `const x = 'a'` type `'a'`?
- [ ] `L2` What does `as const` do?
- [ ] `L2` What is a type assertion (`as`), and why is it dangerous? What is the non-null assertion `!`?
- [ ] `L2` Intersection of two object types with a conflicting property type: what do you get? ↳ property becomes `never`
- [ ] `L2` What is the `object` type vs `Object` vs `{}`? ↳ `{}` accepts any non-nullish value
- [ ] `L2` What are index signatures, and what is the problem with `Record<string, T>` lookups? ↳ returns T even if missing; `noUncheckedIndexedAccess`
- [ ] `L2` What are tuple types, optional and rest elements, and named tuples?
- [ ] `L2` What are function overloads, and when is a union or generic better?
- [ ] `L2` `readonly` properties and `ReadonlyArray`: do they protect you at runtime?
- [ ] `L2` What is type erasure? Why can't you check `if (x instanceof MyInterface)`?
- [ ] `L3` Why is TypeScript's type system unsound on purpose? Give two examples. ↳ array covariance, method bivariance, `any`, index access
- [ ] `L3` What are covariance and contravariance? What does `strictFunctionTypes` change? ↳ parameters checked contravariantly for function-typed props, not methods
- [ ] `L3` What are the `in`/`out` variance annotations on type parameters?

## 7.10 Narrowing, type guards and discriminated unions
**Learn:** https://www.typescriptlang.org/docs/handbook/2/narrowing.html · *Effective TypeScript* (2nd ed) ch.3 "Type Inference and Control Flow Analysis" · Total TypeScript (totaltypescript.com) "Discriminated unions"
- [ ] `L1` What is narrowing? Name five ways to narrow. ↳ typeof, instanceof, in, equality/truthiness, discriminant, type predicate
- [ ] `L1` What is a discriminated (tagged) union?
- [ ] `L2` Write a user-defined type guard (`x is Foo`). What happens if your guard lies?
- [ ] `L2` What is an assertion function (`asserts x is Foo`)? When do you use it?
- [ ] `L2` How do you get exhaustiveness checking in a `switch`? ↳ default branch assigns to `never`; or `satisfies never`
- [ ] `L2` Model an API response that is loading / success with data / error with message as a discriminated union.
- [ ] `L2` Why does narrowing get lost inside a callback? ↳ mutable variable may change; copy to `const`
- [ ] `L2` Why does `typeof x === 'object'` not rule out `null`?
- [ ] `L2` Model payment events (`initiated`, `captured`, `refunded`, `failed`) so invalid combinations cannot be built.
- [ ] `L2` Narrowing with `in`: what are its traps?
- [ ] `L2` Narrow the `unknown` result of `JSON.parse` to a typed object without using `as`.
- [ ] `L2` What does "make illegal states unrepresentable" mean? Give an example from your code.
- [ ] `L3` What are inferred type predicates (TS 5.5), e.g. `arr.filter(x => x !== undefined)`?
- [ ] `L3` How does control-flow analysis work for aliased conditions and destructured discriminants?
- [ ] `L3` Model an LLM agent step (tool call, tool result, final answer, error) as a discriminated union and write the reducer.

## 7.11 Generics and constraints
**Learn:** https://www.typescriptlang.org/docs/handbook/2/generics.html · *Effective TypeScript* (2nd ed) "Generics and Type-Level Programming" ("Think of generics as functions between types") · https://www.totaltypescript.com/books/total-typescript-essentials
- [ ] `L1` What are generics? Why not just use `any`?
- [ ] `L1` What does `<T extends Something>` mean?
- [ ] `L2` Write a typed `getProperty<T, K extends keyof T>(obj: T, key: K)`. What is its return type? ↳ `T[K]`
- [ ] `L2` What is a generic default (`<T = string>`)?
- [ ] `L2` How does TypeScript infer a generic from arguments? When do you have to pass it explicitly?
- [ ] `L2` What is a "useless" generic (type parameter used only once), and why avoid it? ↳ golden rule: type param must relate two things
- [ ] `L2` Write a generic `Repository<T extends { id: string }>` interface with `findById`, `save`, `delete`.
- [ ] `L2` What are `const` type parameters (`<const T>`), and what problem do they solve?
- [ ] `L2` How do you type a function that takes an array and returns its first element, keeping tuple types?
- [ ] `L2` Generic classes vs generic functions: when do you use each?
- [ ] `L2` What is `NoInfer<T>` (TS 5.4) and when do you need it?
- [ ] `L3` Why does `function f<T>(x: T): T` sometimes infer a wider type than you want, and how do you control it?
- [ ] `L3` What is a higher-kinded type, and why can't TypeScript express it directly?
- [ ] `L3` Write `pick<T, K extends keyof T>(obj: T, ...keys: K[]): Pick<T, K>` and explain each part.
- [ ] `L3` Why do too many generics make an API hard to use? How do you keep public signatures simple?

## 7.12 keyof, typeof, indexed access, conditional, mapped and template literal types
**Learn:** https://www.typescriptlang.org/docs/handbook/2/types-from-types.html · https://www.typescriptlang.org/docs/handbook/2/conditional-types.html · https://www.typescriptlang.org/docs/handbook/2/mapped-types.html · https://www.typescriptlang.org/docs/handbook/2/template-literal-types.html
- [ ] `L1` What does `keyof T` give you? What does `typeof value` give you at the type level?
- [ ] `L1` What is an indexed access type (`T['name']`, `T[number]`)?
- [ ] `L1` What is a conditional type (`T extends U ? X : Y`)?
- [ ] `L1` What is a mapped type?
- [ ] `L2` What is `infer`? Write `ElementType<T>` for arrays. ↳ `T extends (infer U)[] ? U : never`
- [ ] `L2` What is a distributive conditional type? What is `ToArray<string | number>`? ↳ distributes: `string[] | number[]`
- [ ] `L2` How do you stop distribution? ↳ wrap in a tuple: `[T] extends [U]`
- [ ] `L2` What does `keyof any` return? ↳ `string | number | symbol`
- [ ] `L2` What are mapping modifiers (`readonly`, `?`, `-readonly`, `-?`)?
- [ ] `L2` What is key remapping with `as` in a mapped type? Write `Getters<T>` producing `getName()` style keys.
- [ ] `L2` What are template literal types? Type an event name like `user:created` from two unions.
- [ ] `L2` What are `Uppercase`, `Lowercase`, `Capitalize`, `Uncapitalize`?
- [ ] `L2` Get the union of values of a `const` object (`(typeof obj)[keyof typeof obj]`).
- [ ] `L3` What happens to a distributive conditional type when you pass `never`? ↳ result is `never` (empty union)
- [ ] `L3` Write `DeepPartial<T>` and `DeepReadonly<T>`. What about arrays and functions?
- [ ] `L3` Write `Paths<T>` that produces all dot paths (`"user.address.city"`) of a nested object.
- [ ] `L3` Parse a route string like `/users/:id/posts/:postId` into `{ id: string; postId: string }` with template literal types.
- [ ] `L3` What are recursive type limits ("type instantiation is excessively deep") and how do you avoid them?
- [ ] `L3` Type-level code makes `tsc` slow. How do you find and fix slow types? ↳ `--extendedDiagnostics`, `--generateTrace`, simpler types, interfaces over intersections

## 7.13 Utility types — use them and implement them
**Learn:** https://www.typescriptlang.org/docs/handbook/utility-types.html · https://github.com/type-challenges/type-challenges (easy + medium)
- [ ] `L1` What do `Partial`, `Required`, `Readonly` and `Record` do?
- [ ] `L1` What do `Pick` and `Omit` do?
- [ ] `L1` What do `Exclude`, `Extract` and `NonNullable` do?
- [ ] `L1` What do `ReturnType`, `Parameters` and `Awaited` do?
- [ ] `L2` Implement `MyPick<T, K>`. ↳ `{ [P in K]: T[P] }` with `K extends keyof T`
- [ ] `L2` Implement `MyPartial<T>` and `MyReadonly<T>`.
- [ ] `L2` Implement `MyOmit<T, K>`. Why is the built-in `Omit` not strict about `K`?
- [ ] `L2` Implement `MyExclude<T, U>` and explain why it relies on distribution.
- [ ] `L2` Implement `MyReturnType<T>` and `MyParameters<T>` with `infer`.
- [ ] `L2` Implement `MyAwaited<T>` that unwraps nested promises.
- [ ] `L2` Implement `MyRecord<K, V>`.
- [ ] `L2` What are `InstanceType`, `ConstructorParameters` and `ThisType`?
- [ ] `L2` Create a DTO type for "update user" from the `User` type: all optional, without `id` and `createdAt`.
- [ ] `L3` Implement `TupleToUnion<T>`, `First<T>`, `Last<T>` and `Length<T>`.
- [ ] `L3` Implement `UnionToIntersection<U>`. ↳ contravariant inference position of function parameters
- [ ] `L3` Implement `IsNever<T>` and explain why `T extends never` alone fails.
- [ ] `L3` Implement `Equals<A, B>` (the one type-challenges uses) and explain why it is tricky.
- [ ] `L3` Implement `Trim<S>` and `Split<S, D>` with template literal types.
- [ ] `L3` Implement `Mutable<T>` and `RequiredKeys<T>` (keys that are not optional).

## 7.14 Branded types, Result types and error handling
**Learn:** *Effective TypeScript* (2nd ed) "Use brands for nominal typing" · https://www.totaltypescript.com/branded-types · https://github.com/supermacro/neverthrow · https://effect.website
- [ ] `L1` What is a branded (nominal) type? Why would you want one?
- [ ] `L1` What is a `Result<T, E>` (Either) type?
- [ ] `L2` Write a `UserId` brand so a `string` or an `OrderId` cannot be passed where a `UserId` is expected. ↳ `string & { readonly __brand: 'UserId' }` + constructor function
- [ ] `L2` Where do you create branded values safely? ↳ one validating constructor/parse function at the boundary
- [ ] `L2` Brand money amounts in paise vs rupees, or validated emails. Give two more real examples.
- [ ] `L2` Write a `Result<T, E>` type plus `ok`, `err`, `map` and `andThen`.
- [ ] `L2` Exceptions vs Result types: trade-offs in a NestJS/Express service.
- [ ] `L2` Why is the type of `e` in `catch (e)` `unknown` (with `useUnknownInCatchVariables`), and how do you handle it?
- [ ] `L2` How do you model expected domain errors vs unexpected bugs in TS?
- [ ] `L2` How do you type custom error classes, and why set `name` and use `cause`?
- [ ] `L2` How do you make an async function return `Promise<Result<T, E>>` and never throw?
- [ ] `L3` How do you combine many `Result`s (like `Promise.all` but for results), and type it?
- [ ] `L3` neverthrow vs Effect vs plain exceptions: when would you adopt a library?
- [ ] `L3` Unique symbols as brands vs string literal brands: differences.
- [ ] `L3` Build a `Result`-returning wrapper around an LLM call that distinguishes rate limit, timeout, invalid JSON and refusal.

## 7.15 Enums, `as const`, `satisfies`, declaration merging and `.d.ts`
**Learn:** https://www.typescriptlang.org/docs/handbook/enums.html · https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html (satisfies) · https://www.typescriptlang.org/docs/handbook/declaration-merging.html · https://www.typescriptlang.org/docs/handbook/declaration-files/introduction.html
- [ ] `L1` What is an enum? Numeric vs string enums.
- [ ] `L1` What does `satisfies` do? How is it different from a type annotation?
- [ ] `L1` What is a `.d.ts` file?
- [ ] `L2` Enums vs union of string literals vs `as const` objects: which do you use and why? ↳ unions/`as const` are erased; enums emit code, numeric enums unsafe
- [ ] `L2` What are `const enum`s and why do some teams ban them? ↳ inlined; break with isolatedModules/Babel/SWC
- [ ] `L2` Why are numeric enums type-unsafe (any number is assignable in older TS)?
- [ ] `L2` Show a case where `satisfies` keeps a narrower type than `: Type` would. ↳ config object keeps literal keys while checked
- [ ] `L2` What is declaration merging? Which declarations can merge?
- [ ] `L2` How do you add a `user` property to Express's `Request` type? ↳ module augmentation: `declare global` / `declare module 'express-serve-static-core'`
- [ ] `L2` How do you type a JS library that has no types? ↳ `@types/x`, write `declare module 'x'`, minimal `.d.ts`
- [ ] `L2` What is `declare`? What is ambient context?
- [ ] `L2` What is DefinitelyTyped, and what goes wrong when `@types` versions drift from the library?
- [ ] `L3` What are namespaces, and why are they rarely used today?
- [ ] `L3` How do you publish a library with correct types for both ESM and CJS consumers? ↳ `exports` with `types` conditions, check with arethetypeswrong
- [ ] `L3` What is `erasableSyntaxOnly` and Node's built-in type stripping, and why do they push teams away from enums?

## 7.16 tsconfig and strict flags
**Learn:** https://www.typescriptlang.org/tsconfig · *Effective TypeScript* (2nd ed) Item "Know which TypeScript options you're using" · https://github.com/tsconfig/bases
- [ ] `L1` What does `"strict": true` turn on? ↳ noImplicitAny, strictNullChecks, strictFunctionTypes, strictBindCallApply, strictPropertyInitialization, etc.
- [ ] `L1` What does `strictNullChecks` do?
- [ ] `L1` What does `noImplicitAny` do?
- [ ] `L2` What does `noUncheckedIndexedAccess` do, and why is it not part of `strict`?
- [ ] `L2` What do `exactOptionalPropertyTypes`, `noImplicitOverride` and `noPropertyAccessFromIndexSignature` do?
- [ ] `L2` What do `target`, `lib`, `module` and `moduleResolution` control?
- [ ] `L2` What is `isolatedModules`, and why do esbuild/SWC/Babel need it?
- [ ] `L2` `tsc` vs ts-node vs tsx vs SWC vs esbuild: which type-checks and which only strips types?
- [ ] `L2` What are `skipLibCheck`, `esModuleInterop` and `allowSyntheticDefaultImports`?
- [ ] `L2` What are project references and `composite`? When do monorepos need them?
- [ ] `L2` What are `paths` aliases, and why do they break at runtime without extra tooling?
- [ ] `L2` What is `strictPropertyInitialization`, and how do NestJS DTOs and TypeORM entities deal with it? ↳ definite assignment `!`, constructor init
- [ ] `L3` Which strict flags would you turn on first in a legacy codebase, and in what order?
- [ ] `L3` How do you keep type-checking fast in CI for a large repo? ↳ incremental, project refs, `tsc --noEmit` separate from build
- [ ] `L3` What does Node's native TypeScript support (type stripping) do and not do?

## 7.17 Runtime validation and type-safe APIs (Zod, typed clients, typed events, builders)
**Learn:** https://zod.dev · https://www.totaltypescript.com/tutorials/zod · https://trpc.io/docs · https://github.com/colinhacks/zod#type-inference · https://docs.nestjs.com/techniques/validation
- [ ] `L1` Why do you need runtime validation if you have TypeScript?
- [ ] `L1` What is Zod? What does `z.infer` give you?
- [ ] `L2` Where must you validate at runtime? ↳ HTTP input, env vars, queue messages, third-party API responses, LLM JSON output
- [ ] `L2` `parse` vs `safeParse` in Zod.
- [ ] `L2` Zod vs class-validator + class-transformer (NestJS) vs Pydantic: compare.
- [ ] `L2` How do you validate and type `process.env` at startup?
- [ ] `L2` How do you validate structured JSON output from an LLM with Zod, and what do you do when it fails? ↳ safeParse, repair/retry with error, JSON schema in prompt
- [ ] `L2` What is `z.discriminatedUnion`, and why is it faster and clearer than `z.union`?
- [ ] `L2` Single source of truth: schema → type, or type → schema? Trade-offs.
- [ ] `L2` How do you share request/response types between a NestJS backend and a React frontend?
- [ ] `L2` What do OpenAPI codegen, tRPC and ts-rest each give you?
- [ ] `L3` Design a type-safe API client: given a route map type, `client.get('/users/:id')` infers params and response.
- [ ] `L3` Design a typed EventEmitter where `emit('order.created', payload)` checks payload by event name.
- [ ] `L3` Design a builder with progressive narrowing: `.select()` must be called before `.build()` compiles.
- [ ] `L3` Validation cost: when does validating every message in a hot Kafka consumer hurt, and what do you do?
- [ ] `L3` How do you version and evolve schemas shared by several services without breaking old clients?

## 7.18 Migrating JavaScript to TypeScript (tie to Jigsaw)
**Learn:** https://www.typescriptlang.org/docs/handbook/migrating-from-javascript.html · *Effective TypeScript* (2nd ed) ch.10 "Modernization and Migration" · https://github.com/airbnb/ts-migrate
- [ ] `L1` Why would a team move a Node.js codebase from JS to TS?
- [ ] `L2` How did you migrate Jigsaw to TypeScript incrementally? Walk me through the steps.
- [ ] `L2` What do `allowJs` and `checkJs` do, and how do JSDoc types help during migration?
- [ ] `L2` Big-bang rewrite vs file-by-file migration: trade-offs.
- [ ] `L2` In which order do you convert modules? ↳ leaves first (utils, models), up the dependency graph
- [ ] `L2` How do you stop new `any` from creeping in? ↳ lint rules (`no-explicit-any`), CI type-check, tracking `any` count
- [ ] `L2` What broke at runtime during the migration even though it type-checked?
- [ ] `L2` How do you type a big legacy object that changes shape across the code?
- [ ] `L2` How did you handle runtime data (request bodies, DB documents) that the new types could not guarantee?
- [ ] `L2` How do you migrate a Mongoose / Sequelize model layer to typed models?
- [ ] `L2` How did you get the team to adopt TS (reviews, conventions, training)?
- [ ] `L2` How do you keep shipping features while the migration is half done?
- [ ] `L3` How do you measure migration progress and type coverage? ↳ files converted, `any` count, type-coverage tool, strict flags enabled
- [ ] `L3` What would you do differently if you migrated again?
- [ ] `L3` How did the migration change bug rates or onboarding time? What numbers can you share?

## 7.19 DI without frameworks, decorators and NestJS metadata
**Learn:** https://docs.nestjs.com/providers · https://docs.nestjs.com/fundamentals/custom-providers · https://www.typescriptlang.org/docs/handbook/decorators.html · https://github.com/rbuckton/reflect-metadata · https://github.com/tc39/proposal-decorators
- [ ] `L1` What is dependency injection? Why use it?
- [ ] `L1` What is a decorator in TypeScript?
- [ ] `L2` Implement DI without a framework (constructor injection + a composition root). ↳ wire dependencies in main; pass interfaces in
- [ ] `L2` Manual DI vs a container (NestJS, InversifyJS, tsyringe): trade-offs.
- [ ] `L2` How does NestJS know what to inject into a constructor? ↳ `emitDecoratorMetadata` writes `design:paramtypes`; `reflect-metadata` reads it
- [ ] `L2` Why can't NestJS inject by interface, and what do you use instead? ↳ interfaces erased; injection tokens with `@Inject`
- [ ] `L2` How do NestJS decorators like `@Controller()` and `@Get()` register routes?
- [ ] `L2` Write a custom NestJS decorator (`@CurrentUser()`) and a custom method decorator (`@Timed()`).
- [ ] `L2` What are provider scopes (singleton, request, transient) and what does request scope cost?
- [ ] `L2` What is a circular dependency in NestJS, and how does `forwardRef` work? Why is it a smell?
- [ ] `L2` Legacy `experimentalDecorators` vs standard (TC39 stage 3) decorators: what changed?
- [ ] `L2` How does DI make unit testing easier? Show a test with a fake repository.
- [ ] `L3` Write a class decorator and a property decorator that store metadata, and a function that reads it.
- [ ] `L3` Why do standard decorators not support parameter decorators, and what does that mean for NestJS?
- [ ] `L3` How would you implement a tiny DI container with tokens and singleton scope in 40 lines?
- [ ] `L3` Functional core / imperative shell vs class-based DI in TypeScript: which do you prefer for an AI agent harness and why?

## 7.20 Rapid-fire round
- [ ] `L1` `typeof null`?
- [ ] `L1` `typeof NaN`?
- [ ] `L1` `NaN === NaN`?
- [ ] `L1` `null == undefined`?
- [ ] `L1` `Number(null)`?
- [ ] `L1` `Number(undefined)`?
- [ ] `L1` `Number("")`?
- [ ] `L1` `0 ?? 5` and `0 || 5`?
- [ ] `L1` Is `[]` truthy?
- [ ] `L1` `"3" * "4"`?
- [ ] `L1` `0.1 + 0.2 === 0.3`?
- [ ] `L1` Largest safe integer?
- [ ] `L1` Is `let` hoisted?
- [ ] `L1` Can you reassign a `const` object's property?
- [ ] `L1` Arrow functions: own `this` or lexical `this`?
- [ ] `L1` Does `bind` call the function?
- [ ] `L1` What does `new` return if the constructor returns a primitive?
- [ ] `L1` `for…of` or `for…in` for array values?
- [ ] `L1` Does `structuredClone` copy functions?
- [ ] `L1` Is `Object.freeze` deep?
- [ ] `L1` `require` is sync or async?
- [ ] `L1` What does `^` allow in semver?
- [ ] `L1` Transpiler or polyfill: adds `Array.prototype.at` to old engines?
- [ ] `L1` `any` or `unknown` — which forces a check before use?
- [ ] `L1` What type does a function that always throws return?
- [ ] `L1` Can an `interface` describe a union?
- [ ] `L1` Do TypeScript types exist at runtime?
- [ ] `L1` What does `keyof { a: 1; b: 2 }` give?
- [ ] `L1` `Partial<T>` makes properties what?
- [ ] `L1` Which utility type removes `null` and `undefined`?
- [ ] `L1` Which flag makes `arr[i]` include `undefined`?
- [ ] `L1` Does `satisfies` change the inferred type?
- [ ] `L1` What does `z.infer` return?
- [ ] `L1` Which package lets NestJS read constructor parameter types?
