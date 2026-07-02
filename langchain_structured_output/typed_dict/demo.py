from typing import TypedDict

class Person(TypedDict):
    name: str
    age: int
    
new_person:Person = {'name': 'Abrar', 'age': 38}

print(new_person)