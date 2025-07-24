# JavaScript Fundamentals

A comprehensive guide to JavaScript data types and type conversions.

## Data Types

JavaScript has several primitive data types and reference types:

### Primitive Types

- **Number**: Represents both integer and floating-point numbers
  - Range: `-(2^53-1)` to `(2^53-1)`
  - Example: `42`, `3.14`, `-17`

- **BigInt**: Supports integers of arbitrary length
  - Example: `9007199254740991n`, `123456789012345678901234567890n`

- **String**: Represents textual data
  - Example: `"Hello World"`, `'JavaScript'`, `` `Template literal` ``

- **Boolean**: Represents logical values
  - Values: `true` or `false`

- **Null**: Represents "nothing" or "empty"
  - **Note**: `null` is not a "reference to a non-existing object" or a "null pointer"
  - Example: `null`

- **Undefined**: Represents unassigned values
  - **Meaning**: "value is not assigned"
  - If a variable is declared but not assigned, its value is `undefined`
  - Example: `undefined`

### Reference Types

- **Object**: Collection of key-value pairs
  - Example: `{ name: "John", age: 30 }`

- **Symbol**: Unique and immutable primitive value
  - Example: `Symbol("description")`

## Type Conversions

### Number Conversions

When converting values to numbers, JavaScript follows these rules:

| Input Value | Result |
|-------------|--------|
| `undefined` | `NaN` |
| `null` | `0` |
| `true` | `1` |
| `false` | `0` |
| `string` | Whitespaces from start and end are removed. If remaining string is empty, result is `0`. Otherwise, number is "read" from string. An error gives `NaN`. |

**Examples:**
```javascript
Number(undefined)  // NaN
Number(null)       // 0
Number(true)       // 1
Number(false)      // 0
Number("  123  ")  // 123
Number("")         // 0
Number("abc")      // NaN
```

### Boolean Conversions

When converting values to booleans, JavaScript follows these rules:

**Falsy values** (become `false`):
- `0`
- Empty string `""`
- `null`
- `undefined`
- `NaN`

**Truthy values** (become `true`):
- All other values including:
  - Non-zero numbers
  - Non-empty strings
  - Objects
  - Arrays
  - Functions

**Examples:**
```javascript
Boolean(0)         // false
Boolean("")        // false
Boolean(null)      // false
Boolean(undefined) // false
Boolean(NaN)       // false
Boolean(42)        // true
Boolean("hello")   // true
Boolean({})        // true
Boolean([])        // true
```

## Quick Reference

### Type Checking
```javascript
typeof 42          // "number"
typeof "hello"     // "string"
typeof true        // "boolean"
typeof null        // "object" (this is a known JavaScript quirk)
typeof undefined   // "undefined"
typeof {}          // "object"
typeof Symbol()    // "symbol"
```

### Type Conversion Methods
```javascript
String(value)      // Convert to string
Number(value)      // Convert to number
Boolean(value)     // Convert to boolean
```

---



# JavaScript Notes

## Type Conversion and Comparisons

### Number Conversion with null and undefined

```javascript
Number(null) // -> 0
Number(null) >= 0 // true
Number(null) == 0 // false
Number(undefined) // -> NaN
```

**Note:** The reason `Number(null) >= 0` returns `true` is that equality checks (`==`) and comparisons (`>`, `<`, `>=`, `<=`) work differently. Comparisons convert `null` to a number, treating it as `0`.

### Undefined Comparisons

```javascript
alert(undefined > 0);  // false (1)
alert(undefined < 0);  // false (2)
alert(undefined == 0); // false (3)
```

- Comparisons (1) and (2) return `false` because `undefined` gets converted to `NaN` and `NaN` is a special numeric value which returns `false` for all comparisons.
- The equality check (3) returns `false` because `undefined` only equals `null`, `undefined`, and no other value.

### Special Relationship: undefined and null

```javascript
undefined == null // true (magical couple)
```

## Boolean Conversion

### Double NOT Operator (!!)

A double NOT `!!` is sometimes used for converting a value to boolean type:

```javascript
alert(!!"non-empty string"); // true
alert(!!null);               // false
```

## Nullish Coalescing Operator (??)

The nullish coalescing operator is written as two question marks `??`.

As it treats `null` and `undefined` similarly, we'll use a special term here: a value is "defined" when it's neither `null` nor `undefined`.

The result of `a ?? b` is:
- if `a` is defined, then `a`
- if `a` isn't defined, then `b`

## Transpilers and Polyfills

### Transpilers

A **transpiler** is a special piece of software that translates source code to another source code. It can parse ("read and understand") modern code and rewrite it using older syntax constructs, so that it'll also work in outdated engines.

**Example:** JavaScript before year 2020 didn't have the "nullish coalescing operator" `??`. So, if a visitor uses an outdated browser, it may fail to understand the code like `height = height ?? 100`.

A transpiler would analyze our code and rewrite `height ?? 100` into `(height !== undefined && height !== null) ? height : 100`.

### Polyfills

In some cases, using new functions like `Math.trunc()` is not present in old browsers. **Polyfills** add the missing function implementations.

### When to Use

Using webpack or TypeScript needs transpilers and polyfills, as they need to convert the code. The build process will check the browser supported versions and modify those that are not supported by the browser. 