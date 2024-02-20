namespace py example

struct Person {
  1: string name,
  2: i32 age,
  3: string email
}

service PersonService {
  void addPerson(1: Person person),
  Person getPerson(1: string name)
}
