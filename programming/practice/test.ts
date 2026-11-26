interface Person {
first: string;
lastName: string;
}
const formatName = (p: Person) =>`${p.first} ${p.lastName}`
const formatNameAny = (p: Person) =>`${p.first} ${p.lastName}`;