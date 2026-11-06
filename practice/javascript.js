// // This code lives in examples/v8/hidden-classes-demo.js

// // Run with: node --allow-natives-syntax hidden-classes-demo.js
// const obj1 = {};
// console.log(%HaveSameMap(obj1, {})); // true. Both share the initial hidden class.
// %DebugPrint(obj1); // Initial hidden class.

// // Adding a property creates a new hidden class and a transition.
// obj1.x = 1;
// %DebugPrint(obj1); // Initial hidden class.


// const obj2 = {};
// console.log(%HaveSameMap(obj1, obj2)); // false. obj1's hidden class has changed.

// obj2.x = 5;
// // Now obj2 has followed the same transition path as obj1.
// console.log(%HaveSameMap(obj1, obj2)); // true. They now share the same hidden class again.


// const obj1 = {};
// console.log(Object.getPrototypeOf(obj1));
// console.log(Object.getOwnPropertyNames(obj1));
// console.log(Object.prototype);
// console.log(obj1.__proto__);


const buf = Buffer.from([72, 73])
console.log(buf.toString("utf8")); // Output: Hello, World!