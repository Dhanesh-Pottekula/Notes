// class Person{
//     constructor(name,age){
//         this.name = name
//         this.age = age
//     }
    
//     introduce(){
//         console.log('HELLO, MY NAME IS ' + this.name + ' AND I AM ' + this.age + ' YEARS OLD ')
//     }
// }

// const person1 = new Person('Alice', 30)
// person1.introduce()

// class Employ extends Person{
//     constructor(name,age,job){
//         super(name,age)
//         this.job = job
//     }
//     introduce_emp (){
//         console.log("hello i am " + this.name+"age"+this.age + "job "+ this.job )
//     }
// }

// const Employ1 = new Employ("dhaensh",25,"full stack")
// Employ1.introduce_emp()
// Employ1.introduce()


// this the class constructor implementation
const Person2 = function (name,age){
    this.name= name 
    this.age= age
}

// add the method into it 
Person2.prototype.introduce=function (){
    console.log('HELLO, MY NAME IS ' + this.name + ' AND I AM ' + this.age + ' YEARS OLD ')
}

const person2 = new Person2("dhanesh",22);
// person2.introduce()

// calling the constructor of 2 classes (using super() )

//notes : with out the new key word this is treated as just another function so the Employ2 will be undefined as the function is not returing anything 
// if you return any. primitive types like string , number , bigint, undefined, null, symbol ,bool then it will work fine with new keyword as the "this " instance returned  by the funciton
// but if you return the {} then it will replace the "this" then it will fail to access any methods as {} will not have any methods
const Employ2 = function (name,age,job){
    this.job=job
    Person2.call(this,name,age)
}
Employ2.prototype.introduce_e=function(){
    console.log(this.job)
}

// extends settings the prototype of employ2 -> person prototype instead of Obeject
Object.setPrototypeOf(Employ2.prototype, Person2.prototype);

const employ2 =  new Employ2("dhanesh",22,"soft")
employ2.introduce()
employ2.introduce_e()
console.log(employ2)