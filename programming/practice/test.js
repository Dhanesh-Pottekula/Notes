const user = {
  name: "Dhanesh",
  greet() {
    function inner() {
      console.log(this.name);
    }
    inner();
  }
};

console.log(user.greet());