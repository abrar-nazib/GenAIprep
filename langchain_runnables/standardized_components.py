import random
from abc import ABC, abstractmethod
import warnings


class Runnable(ABC):
    @abstractmethod
    def invoke(self, input_data):
        pass


class FakeLLM(Runnable):
    def __init__(self):
        print("LLM Created")

    def invoke(self, prompt):
        response_list = ["Response 1", "Response 2", "Response 3"]
        return {"response": f"{prompt} --- {random.choice(response_list)}"}

    def predict(self, prompt):
        warnings.warn(
            "predict() is deprecated; use invoke() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.invoke(prompt)


class FakePromptTemplate(Runnable):
    def __init__(self, template, input_variables):
        self.template = template
        self.input_variables = input_variables

    def invoke(self, input_data):
        return self.template.format(**input_data)

    def format(self, input_data):
        warnings.warn(
            "format() is deprecated; use invoke() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.invoke(input_data)


class FakeStrOutputParser(Runnable):
    def invoke(self, input_data: dict):
        return input_data.get("response", "")


class RunnableConnector(Runnable):
    def __init__(self, runnable_list):
        self.runnable_list = runnable_list

    def invoke(self, input_data):
        for runnable in self.runnable_list:
            input_data = runnable.invoke(input_data)
        return input_data


llm = FakeLLM()
template = FakePromptTemplate(
    template="Write a {length} poem about {topic}.",
    input_variables=["length", "topic"],
)
parser = FakeStrOutputParser()

chain = RunnableConnector([template, llm, parser])
output = chain.invoke({"length": "short", "topic": "football"})
print(output)  # Expected: Write a short poem about football. --- Response 3
