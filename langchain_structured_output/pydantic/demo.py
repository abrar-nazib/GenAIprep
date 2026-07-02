from langchain_openrouter import ChatOpenRouter
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from dotenv import load_dotenv
import os

cwd = os.path.dirname(__file__)
load_dotenv(os.path.join(cwd, ".env"))


class Student(BaseModel):
    name: str = "Student"
    age: Optional[int] = None
    email: EmailStr
    cgpa: float = Field(gt=0, le=4, default=3.00, description="A decimal value representing the cgpa of the student")  # Constraint and description


new_student = {"name": "abrar", "email": "abrarnazib@gmail.com", "cgpa" : "3.21"}
student = Student(**new_student)

print(type(student))
print(student.name)
print(student.model_dump_json())
